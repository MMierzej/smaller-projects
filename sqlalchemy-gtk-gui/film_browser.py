import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine


Base = declarative_base()

class InvalidYearException(Exception):
    pass

class FilmAlreadyExistsException(Exception):
    pass

class FilmDoesntExistException(Exception):
    pass

class EmptyInfoException(Exception):
    pass

class Film(Base):
    """Class that stores info about films."""
    __tablename__ = 'films'

    id_film = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer)
    title = Column(String)
    director = Column(String)
    operator = Column(String)
    producer = Column(String)

    def __init__(self, title, year, director, operator, producer):
        """All arguments should be strings except `year` which should a non-negative integer not larger than 2021."""
        if not str(year).isnumeric() or not int(str(year)) <= 2021:
            raise InvalidYearException()

        self.year = int(str(year))
        self.title = title
        self.director = director
        self.operator = operator
        self.producer = producer
    
    def __str__(self):
        return f'"{self.title}" by {self.director}, {self.year}, operator: {self.operator}, producer: {self.producer}'

class View:
    """Class that handles GUI for this application."""
    def __init__(self, glade_file='film_browser.glade', films=[]):
        self.builder = gtk.Builder()
        self.builder.add_from_file(glade_file)

        self.window = self.builder.get_object('main_window')

        # components of list of films
        self.treeview   = self.builder.get_object('treeview_items')
        self.selection  = self.treeview.get_selection()
        self.films_list = self.builder.get_object('films_list')

        # full-info widget componenets
        self.year_label = self.builder.get_object('year_label')
        self.title_label = self.builder.get_object('title_label')
        self.director_label = self.builder.get_object('director_label')
        self.operator_label = self.builder.get_object('operator_label')
        self.producer_label = self.builder.get_object('producer_label')

        # buttons
        self.rm_btn = self.builder.get_object('rm_btn')
        self.add_btn = self.builder.get_object('add_btn')
        self.edit_btn = self.builder.get_object('edit_btn')
        self.rmsel_btn = self.builder.get_object('rmsel_btn')

        # entries
        self.year_entry = self.builder.get_object('year_entry')
        self.title_entry = self.builder.get_object('title_entry')
        self.director_entry = self.builder.get_object('director_entry')
        self.operator_entry = self.builder.get_object('operator_entry')
        self.producer_entry = self.builder.get_object('producer_entry')

        # actions menu components
        self.menu_rm = self.builder.get_object('menu_rm')
        self.menu_add = self.builder.get_object('menu_add')
        self.menu_clr = self.builder.get_object('menu_clr')
        self.menu_edit = self.builder.get_object('menu_edit')

        # connecting actions
        self.selection.connect('changed', self.set_full_info)
        self.window.connect('destroy', gtk.main_quit)

        self.update_films_list(films)

    def set_full_info(self, widget):
        """Sets the display of full info (in a separate widget) about the selected film."""
        model, treeiter = widget.get_selected()
        if treeiter is not None:
            film = model[treeiter][:]
            self.title_label.   set_text(film[0])
            self.director_label.set_text(film[1])
            self.year_label.    set_text(film[2])
            self.operator_label.set_text(film[3])
            self.producer_label.set_text(film[4])
        else:
            self.title_label.   set_text('Title')
            self.director_label.set_text('Director')
            self.year_label.    set_text('Year')
            self.operator_label.set_text('Operator')
            self.producer_label.set_text('Producer')
        self.refresh()

    def update_films_list(self, films=[]):
        """Displays all films contained in the database in a single scrollable list of items."""
        self.films_list.clear()  # clears the current list
        for film in films:  # repopulates the list with currently stored films
            self.films_list.append((film.title, film.director, str(film.year), film.operator, film.producer))
    
    def reset_entries(self):
        self.year_entry.set_text('')
        self.title_entry.set_text('')
        self.director_entry.set_text('')
        self.operator_entry.set_text('')
        self.producer_entry.set_text('')

    def refresh(self):
        self.window.show_all()

class Controller:
    """
    Objects of this class glue GUI and database operations together.
    """
    def __init__(self, handler, view):
        self.handler = handler
        self.view = view

        self.view.rm_btn.connect('clicked', self.remove_films_from_db)  # triggers removal of the items that satisfy the constraints given in the entries
        self.view.add_btn.connect('clicked', self.add_film_to_db)  # triggers addition of the film that is described by the entries' content
        self.view.edit_btn.connect('clicked', self.edit_film_in_db)  # triggers the edition of the selected element
        self.view.rmsel_btn.connect('clicked', lambda widget: self.remove_films_from_db(widget, True))  # triggers the removal of the selected element

        self.view.menu_rm.connect('activate', lambda widget: self.remove_films_from_db(widget, True))  # triggers removal of the items that satisfy the constraints given in the entries
        self.view.menu_clr.connect('activate', lambda widget: self.remove_films_from_db(widget, False, True))  # triggers removal of all films
        self.view.menu_add.connect('activate', self.add_film_to_db)  # triggers addition of the film that is described by the entries' content
        self.view.menu_edit.connect('activate', self.edit_film_in_db)  # triggers the edition of the selected element

        self.update_view()

    def add_film_to_db(self, widget):
        """
        Adds a film to the database, whose info is sourced from the appropriate entry fields.
        All entries must contain at least one non-whitespace character for the given film to be added.
        Year entry must be a non-negative integer no larger than 2021.
        It is not possible to add the same film to the database twice. If there is an attempt of doubling
        an entry, nothing gets added.
        """
        year = self.view.year_entry.get_text().strip()
        title = self.view.title_entry.get_text().strip()
        director = self.view.director_entry.get_text().strip()
        operator = self.view.operator_entry.get_text().strip()
        producer = self.view.producer_entry.get_text().strip()

        try:
            self.handler.add_film(title, year, director, operator, producer)
            self.view.films_list.append((title, director, year, operator, producer))
            self.view.reset_entries()
            self.view.refresh()
        except: pass

    def edit_film_in_db(self, widget):
        """
        Editing can be performed only on the selected element. If nothing is selected,
        then no editing is performed.
        Changes to be made are sourced from the appropriate entry fields. If a certain entry field
        is empty (or contains only whitespace), then the respective field of the database entry
        does not get changed.
        """
        model, treeiter = self.view.selection.get_selected()
        if treeiter is None:
            return

        film = model[treeiter][:]
        title    = film[0]
        director = film[1]
        year     = film[2]
        operator = film[3]
        producer = film[4]

        changes = {}
        ch_year = self.view.year_entry.get_text().strip()
        ch_title = self.view.title_entry.get_text().strip()
        ch_director = self.view.director_entry.get_text().strip()
        ch_operator = self.view.operator_entry.get_text().strip()
        ch_producer = self.view.producer_entry.get_text().strip()
        if ch_year: changes['year'] = ch_year
        if ch_title: changes['title'] = ch_title
        if ch_director: changes['director'] = ch_director
        if ch_operator: changes['operator'] = ch_operator
        if ch_producer: changes['producer'] = ch_producer

        try:
            self.handler.edit_film(title, year, director, operator, producer, changes)
            self.view.reset_entries()
            self.update_view()
        except: pass

    def remove_films_from_db(self, widget, selected=False, wipe=False):
        """
        Removal is done either by removing the selected item, or by removing
        all elements from the database that satisfy the constraints given in the entries.
        If all entries are empty and `selected` is `False`, then no removal is performed.
        If `wipe` is true, then the whole database gets cleared.
        `selected` is a flag that informs if removal should be done of the selected element
        instead of films that satisfy the given criteria.
        If `selected` is `True` and nothing is selected, then no removal is performed.
        """
        if selected:
            model, treeiter = self.view.selection.get_selected()
            if treeiter is None:
                return

            film = model[treeiter][:]
            title    = film[0]
            director = film[1]
            year     = film[2]
            operator = film[3]
            producer = film[4]
        else:
            year = self.view.year_entry.get_text().strip()
            title = self.view.title_entry.get_text().strip()
            director = self.view.director_entry.get_text().strip()
            operator = self.view.operator_entry.get_text().strip()
            producer = self.view.producer_entry.get_text().strip()
            if not wipe and not any((title, year, director, operator, producer)):
                return
            self.view.reset_entries()

        try:
            self.handler.remove_films(title, year, director, operator, producer)
            self.update_view()
        except: pass

    def update_view(self):
        """
        Populates the films list with all the films stored in the database.
        """
        self.view.update_films_list(self.handler.find_films())
        self.view.refresh()

class Handler:
    """
    Class that is able to handle database operations made available by this script.
    Those are:
    - adding a film to the database
    - editing an existing database entry
    - finding and listing films whose metainfo fulfill certain criteria
    - removing from the database films whose metainfo fulfill certain criteria
    """

    def __init__(self, session):
        self.session = session

    def add_film(self, title, year, director, operator, producer):
        """Arguments should be strings containing valid metainfo about a film. All arguments are non-optional."""
        if not all((title, director, year, operator, producer)):
            raise EmptyInfoException()

        # checking if the film has already been added to the database
        exists = self.session.query(Film).filter_by(title=title, year=year, director=director, operator=operator, producer=producer).first() is not None
        if exists:
            raise FilmAlreadyExistsException()

        film = Film(title, year, director, operator, producer)
        self.session.add(film)
        self.session.commit()

    def edit_film(self, title, year, director, operator, producer, changes):
        """
        Arguments should be strings containing appropriate and valid info about the edited film, except `changes`.
        `changes` should be a dictionary containing the changes to be made in the film's database entry fields named
        just as 2.-6. arguments of this method. Only explicitly specified fields are changed.
        """
        if not all((title, director, year, operator, producer)):
            raise EmptyInfoException()

        film = self.session.query(Film).filter_by(title=title, year=year, director=director, operator=operator, producer=producer).first()
        if film is None:
            raise FilmDoesntExistException()

        if 'year' in changes:
            year = changes['year']
            if not str(year).isnumeric() or not int(str(year)) <= 2021:  # assuming that a valid year is between 0 and 2021
                raise InvalidYearException()
            film.year = int(str(year))
        if 'title' in changes:    film.title = changes['title']
        if 'director' in changes: film.director = changes['director']
        if 'operator' in changes: film.operator = changes['operator']
        if 'producer' in changes: film.producer = changes['producer']

        self.session.commit()

    def remove_films(self, title=None, year=None, director=None, operator=None, producer=None):
        """Arguments should be valid metainfo about films. A film will be removed if it matches the given criteria."""
        filters = {}
        if year:     filters['year'] = year
        if title:    filters['title'] = title
        if director: filters['director'] = director
        if operator: filters['operator'] = operator
        if producer: filters['producer'] = producer

        to_remove = self.session.query(Film).filter_by(**filters).all()
        for film in to_remove:
            self.session.delete(film)
        self.session.commit()

    def find_films(self, title=None, year=None, director=None, operator=None, producer=None):
        """Arguments should be valid metainfo about films. A film will be listed if it matches the given criteria."""
        filters = {}
        if year:     filters['year'] = year
        if title:    filters['title'] = title
        if director: filters['director'] = director
        if operator: filters['operator'] = operator
        if producer: filters['producer'] = producer
        return self.session.query(Film).filter_by(**filters).all()  # returns a list of found films


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connnection_string = "sqlite:///" + os.path.join(BASE_DIR, 'films.db')
engine = create_engine(connnection_string)
Base.metadata.create_all(bind=engine)
Session = sessionmaker()
sesh = Session(bind=engine)
controller = Controller(Handler(sesh), View())
gtk.main()
sesh.close()
