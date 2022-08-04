import time
import concurrent.futures

import requests
import bs4
from bs4 import *


class Monitor:
    def __init__(self, pages, parser):
        """
        Input:
        `pages` -- list of URLs of HTML-based websites to be monitored
        `parser` -- HTML parser to be used by `bs4` module to parse the HTML tree
        """
        self.pages = pages
        self.parser = parser

    def find_differences(self, before_parent, now_parent, before, now):
        """
        This function finds differences between two elements of some `bs4` classes. It aims to find differences
        between the past and the current version of some HTML-based website (with help of the `bs4` module).
        It traverses the parsed HMTL trees in parallel, looking for differences in corresponding nodes.

        ASSUMPTION: BeautifulSoup always parses in the same way and order
        (in particular: parsing one html text multiple times yields the same result everytime)

        Input:
        All of the below should be objects of classes from the `bs4` module which represent some part of the parsed html.
        `before_parent` -- a parent element, which immediately contains the `before` element or None if starting from the root of the tree
        `now_parent` -- a parent element, which immediately contains the `now` element or None if starting from the root of the tree
        `before` -- an element present in the site's previous version
        `now` -- a present element which is to be compared for differences against the `before` element

        Output:
        A set of tuples, each of tuples contains 4 elements:
        1. `(row, col)` -- contains correspondigly the row and the column at which the `now` element is located in the source code
        2. `(before_parent, row_parent)` -- contains references to corresponding parent element of `before` and `now`
        3. short description of the found changes
        4. `(before, now)` -- the elements themselves at which the change has occured
        Returned objects inside those tuples are from `bs4` module.
        """

        # adding `where` to the result, because that makes the below tuple different,
        # even if other contained elements are equivalent by `bs4` standard comparison
        # this prevents incorrect skipping of elements that actually did change
        parents = (before_parent, now_parent)
        where = (now.sourceline, now.sourcepos) if hasattr(now, 'sourceline') else (None, None)  # NavigableString types do not store information about their position in the source
        elems = (before, now)

        if before and not now:
            return {(where, parents, 'element removed', elems)}
        
        if not before and now:
            return {(where, parents, 'element added', elems)}

        if type(before) != type(now):
            return {(where, parents, 'element type', elems)}

        # according to bs4's documentation, practically only three types are to be checked:
        # NavigableString which can't contain any children
        # Tag which encapsulates an html tag and can contain children
        # BeautifulSoup which can for the most part be treated just like Tag

        # there are special cases of NavigableString, but they don't differ from NavigableString
        # in terms of processing when it comes to comparing two parsed html trees

        if issubclass(type(before), (bs4.element.NavigableString, )):
            # NavigableString cannot contain any children so it is the bottom of the recursion
            return {(where, parents, 'text', elems)} if before != now else set()

        if issubclass(type(before), (bs4.BeautifulSoup, bs4.element.Tag)):
            differences = set()
            # if the layout has changed (elements have been added/removed)
            # then respective contents lists are of different lengths
            len_diff = len(before.contents) - len(now.contents)
            # filling with Nones in case the layout has changed
            # to prevent omitting elements in zip function below
            # by equalizing lengths of two lists
            before_contents = before.contents + [None for _ in range(-len_diff)]
            now_contents = now.contents + [None for _ in range(len_diff)]

            what = []  # list of what has changed here
            if before.name != now.name:
                what.append('type')
            if before.attrs != now.attrs:
                what.append('attributes')
            if what:
                differences.add((where, parents, 'tag ' + ', '.join(what), elems))

            for c1, c2 in zip(before_contents, now_contents):
                differences.update(self.find_differences(before, now, c1, c2))

            return differences

        return set()

    def print_changes(self, changes):
        """
        Prints neatly formatted information about the given changes.

        Input:
        `changes` -- a list that is an output of the `find_differences` method

        Output:
        Returns None. Prints stuff to the console.
        """

        print("Number of changes found:", len(changes))
        print()
        print("===================================================")
        print("===================================================")
        print()

        for (r, c), (pb, pn), what, (b, n) in changes:
            print("Change:", what)
            print("At:", (r, c))
            print()

            print("Changed elements:")
            print("-- before:")
            print(type(b), b.name if b else None)
            print(b)
            print()
            print("-- now:")
            print(type(n), n.name if n else None)
            print(n)
            print()
            print()

            print("Parents:")
            print("-- before:")
            if pb is not None:
                print((pb.sourceline, pb.sourcepos), type(pb), pb.name)
            else:
                print((None, None), type(pb), None)
            print()
            print("-- now:")
            if pn is not None:
                print((pn.sourceline, pn.sourcepos), type(pn), pn.name)
            else:
                print((None, None), type(pn), None)
            print()

            print("===================================================")
            print("===================================================")
            print()

    def monitor_changes(self, interval):
        """
        Monitors content changes in the given websites periodically in given time interval.

        Input:
        `interval` -- time interval in seconds after which the check for changes should take place

        Output:
        Returns None. Prints info about changes to the console.
        If there occurs an error while connecting to the website to be monitored,
        the monitoring is stopped with an adequate message.
        """

        def fetch_soup(page):
            return BeautifulSoup(requests.get(page).text, self.parser)

        def update_soups(executor, soups):
            # modifies `soups`, but is the only thread to do so

            # dict of Futures and corresponding pages
            f_to_page = {executor.submit(fetch_soup, page): page for page in self.pages}
            for f in concurrent.futures.as_completed(f_to_page):  # a queue of completed thread tasks
                try:
                    # this will re-raise an exception if it occured while executing the funciton in a separate thread
                    soup = f.result()
                except:
                    # if there was an error while downloading the site, then the site's value is None
                    # it will be handled later on
                    soup = None  
                page = f_to_page[f]
                # no need for any locks, because this is the main thread
                # no other thread is able to modify any object that belongs to the main thread
                soups[page] = soup
                yield page


        soups = {}
        new_soups = {}
        with concurrent.futures.ThreadPoolExecutor() as thread_executor:  #, concurrent.futures.ProcessPoolExecutor() as process_executor:
            # initialization
            print("Fetching initial data...")
            for page in update_soups(thread_executor, soups):
                continue
            print("Done. Waiting the given time interval...")
            print()

            # monitoring
            while time.sleep(interval) or True:
                t0 = time.perf_counter()
                fp_to_page = {}  # dict of Futures and corresponding pages (used only if submitting diff finding to separate threads)

                print("RESULTS:\n")
                for page in update_soups(thread_executor, new_soups):
                    if new_soups[page] is None:
                        print(f"{page}\nPage unavailable.\n")
                    elif soups[page] is None:
                        print(f"{page}\nPage is now available (previously unavailable).\n")
                    else:
                        before = soups[page]
                        now = new_soups[page]

                        # # the below using processes doesn't work due to the pickling mechanism
                        # # https://www.py4u.net/discuss/225589
                        # # seems like `bs4` objects are unpickleable in some situations (when they are large)
                        # # the below worked fine when tested with `html_doc1` and `html_doc2` which are defined near the bottom of this file
                        # fp = process_executor.submit(self.find_differences, None, None, before, now)
                        # fp_to_page[fp] = page

                        # measurements tell that using threads for those computations is at best
                        # not better than running everything in the main thread one after the other:
                        # about 1.5s of work for multi- and singlethreaded computations.
                        # it is because there exists a Global Interpreter Lock, which effectively
                        # means that only a single thread can run Python code within a Python process.
                        # this means that using threads is productive really only when dealing with I/O-bound problems.
                        # using multiple threads when optimizing the CPU-bound problems can even be counter productive
                        # because of the context switching.
                        # the nature of diff finding is computational, so it doesn't make sense to put it into
                        # separate threads, since only one can be running at a time anyway.
                        # it would be useful if processes worked for diff finding for `bs4` objets, because then CPU cores
                        # would actually run computations in parallel, but it's not viable since `bs4` objects
                        # are unpickleable in real-world situations (when they contain actual parsed websites),
                        # and apparently processes demand pickling of arguments
                        fp = thread_executor.submit(self.find_differences, None, None, before, now)
                        fp_to_page[fp] = page

                        # # single-threaded computations:
                        # diff = self.find_differences(None, None, before, now)
                        # # self.print_changes(diff)
                        # # instead of the above line, for readability:
                        # print(page)
                        # print("Changed:", soups[page] != new_soups[page])  # `bs4`'s built-in comparison
                        # print(len(diff))  # number of changes found by my code
                        # print()

                # when running computations in separate threads/processes this prints the results
                for fp in concurrent.futures.as_completed(fp_to_page):
                    diff = fp.result()
                    page = fp_to_page[fp]
                    # self.print_changes(diff)
                    # instead of the above line, for readability:
                    print(page)
                    print("Changed:", soups[page] != new_soups[page])  # `bs4`'s built-in comparison
                    print(len(diff))  # number of changes found by my code
                    print()

                # swapping references to objects:
                # new_soups become current soups
                # current soups objects will serve as a container for the new incoming soups
                aux = soups
                soups = new_soups
                new_soups = aux

                print(f"Time elapsed: {time.perf_counter() - t0}s")
                print()
                print("===================================================")
                print("===================================================")
                print()

"""
Improvements: the code from the solution of the exercise from the previous list takes ~4.6s to process
the below `pages` list, so the improvement is about 3s. It's hard to tell what is the factor of improvement,
however it seems quite significant.

Thread-safety:
-- in my code: I'm not performing any modifications of shared data structures, no threads modify objects
that belong to the main thread, so there's no need for any use of locks. Also, I think it's completely unnecessary
to introduce shared object modification in my code.

-- in Python in general: there are data structures in Python implemented specifically for thread safety (e.g. Queue),
however in general it is not certain that Python's data structures are thread-safe. Even if for example lists are
thread-safe themselves, data stored in them most likely isn't (https://stackoverflow.com/questions/6319207/are-lists-thread-safe).
An illustration of this is as follows: imagine that a thread within a process acquires a shared variable for modification,
modifies it locally, and before updating the shared state of the variable, it gets substituted with another thread within
the same process. Suppose that the new thread also acquires this shared variable for modification and changes its state locally.
Since the first thread has not yet updated the shared state, the new thread has acquired the variable's state before the modification,
which is in progress in the first thread. Suppose that both considered threads will eventually modify the global state of the variable.
One of them undoubtedly will modify the shared state before the other, so when the second one to update the state overwrites
the shared state, the value from the first thread is already there. The result will be as if the shared variable
has been modified by only one of the two considered threads, when clearly both of them have performed a modification.
For that reason, the best practice is to just implement a mechanism ensuring thread safety each time when performing
a multithreaded code, in which many threads have access to the same data structure. Such mechanisms can be implemented
using locks for example.
"""

"""
# Google's page changes every time, because it generates a one-time numbers for some elements
# The list of WWE's personnel is the most frequently changed Wiki page in the last 15 years
pages = [
    'https://en.wikipedia.org/wiki/List_of_WWE_personnel/',
    'https://www.google.com/',
    'https://wiki.python.org/moin/TimeComplexity/',
    'https://onet.pl/',
    'https://en.wikipedia.org/',
    'https://docs.python.org/3/library/concurrent.futures.html',
    'https://ii.uni.wroc.pl/',
    'https://thiswebsitedoes.notexist/',  # this website did not exist when I was writing this code
    'https://books.toscrape.com/',
    'https://picsum.photos/',
    'https://stackoverflow.com/',
    'https://codeforces.com/'
]

monitor = Monitor(pages, 'html.parser')
monitor.monitor_changes(5)
"""
