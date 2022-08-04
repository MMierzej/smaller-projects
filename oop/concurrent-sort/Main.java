import java.util.Arrays;
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        Random rand = new Random();
        Integer[] array = new Integer[25];

        for (int i = 0; i < 25; i++) {
            array[i] = rand.nextInt(100);
        }

        try {
            ConcurrentSort.concurrentSort(array);
        } catch (Exception e) {
            System.out.println("Sorting has been interrupted.");
        } finally {
            System.out.println(Arrays.toString(array));
        }
    }
}
