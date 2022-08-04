import java.util.Arrays;

public abstract class ConcurrentSort {
    public static <E extends Comparable<E>> E[] concurrentSort(E[] array) throws InterruptedException {
        Thread sort = new SortThread<>(array, 0, array.length - 1);

        sort.start();
        sort.join();

        return array;
    }
    
    private static class SortThread<E extends Comparable<E>> extends Thread {
        private E[] array;
        private int left;
        private int right;

        public SortThread(E[] array, int left, int right) {
            this.array = array;
            this.left = left;
            this.right = right;
        }

        private void merge(int mid) {
            E[] result = Arrays.copyOf(array, array.length);
            int i = left;
            int j = mid + 1;
            int k = left;

            while (i <= mid && j <= right) {
                if (array[i].compareTo(array[j]) < 0) {
                    result[k++] = array[i++];

                } else {
                    result[k++] = array[j++];
                }
            }

            while (i <= mid) {
                result[k++] = array[i++];
            }

            while (j <= right) {
                result[k++] = array[j++];
            }

            while (--k >= left) {
                array[k] = result[k];
            }
        }
        
        public void run() {
            int mid = (right - left) / 2 + left;

            if (left < right) {
                Thread sortLeft = new SortThread<>(array, left, mid);
                Thread sortRight = new SortThread<>(array, mid + 1, right);

                sortLeft.start();
                sortRight.start();

                try {
                    sortLeft.join();
                    sortRight.join();
                    merge(mid);
                } catch (InterruptedException e) {
                    System.out.println("Sorting interrupted.");
                    // throw new InterruptedException();
                }
            }
        }
    }
}
