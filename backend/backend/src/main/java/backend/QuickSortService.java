package backend;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Service
public class QuickSortService {

    /**
     * Hoare quicksort with median-of-three pivot (fixed strategy) and full step trace.
     */
    public SortResponse sort(List<Integer> input) {
        return new SortRun().execute(input);
    }

    /**
     * One sort invocation: all mutable trace state is local, so {@link QuickSortService} stays thread-safe.
     */
    private static final class SortRun {
        private final List<SortStep> steps = new ArrayList<>();
        private int comparisons = 0;
        private int swaps = 0;
        private int maxDepth = 0;
        private final Set<Integer> sortedIndices = new HashSet<>();

        SortResponse execute(List<Integer> input) {
            int[] arr = input.stream().mapToInt(Integer::intValue).toArray();
            long start = System.currentTimeMillis();
            quickSort(arr, 0, arr.length - 1, 0);
            long elapsed = System.currentTimeMillis() - start;
            return new SortResponse(steps, comparisons, swaps, maxDepth, elapsed);
        }

        private void quickSort(int[] arr, int low, int high, int depth) {
            if (depth > maxDepth) {
                maxDepth = depth;
            }

            if (low < high) {
                int pivotIndex = hoarePartition(arr, low, high, depth);
                quickSort(arr, low, pivotIndex, depth + 1);
                quickSort(arr, pivotIndex + 1, high, depth + 1);
            } else if (low == high) {
                sortedIndices.add(low);
                recordStep(arr, null,
                        List.of(), List.of(), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Index " + low + " (" + arr[low] + ") is in its final position");
            }
        }

        private int hoarePartition(int[] arr, int low, int high, int depth) {
            int pivotValue = medianOfThree(arr, low, high, depth);
            int pivotIdx = high;

            int left = low - 1;
            int right = high + 1;

            while (true) {
                do {
                    left++;
                    comparisons++;
                    recordStep(arr, pivotIdx,
                            List.of(left), List.of(), new ArrayList<>(sortedIndices),
                            low, high, depth,
                            "Comparing arr[" + left + "] (=" + arr[left] + ") with pivot " + pivotValue);
                } while (arr[left] < pivotValue);

                do {
                    right--;
                    comparisons++;
                    recordStep(arr, pivotIdx,
                            List.of(right), List.of(), new ArrayList<>(sortedIndices),
                            low, high, depth,
                            "Comparing arr[" + right + "] (=" + arr[right] + ") with pivot " + pivotValue);
                } while (arr[right] > pivotValue);

                if (left >= right) {
                    recordStep(arr, pivotIdx,
                            List.of(), List.of(), new ArrayList<>(sortedIndices),
                            low, high, depth,
                            "Partitioning complete (Hoare). Split index " + right
                                    + ": subarray [" + low + ".." + right + "] and [" + (right + 1) + ".." + high + "].");
                    return right;
                }

                swap(arr, left, right);
                swaps++;
                recordStep(arr, pivotIdx,
                        List.of(), List.of(left, right), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Swapped arr[" + left + "] (=" + arr[left] + ") and arr[" + right + "] (=" + arr[right] + ")");
            }
        }

        private int medianOfThree(int[] arr, int low, int high, int depth) {
            int mid = (low + high) / 2;

            if (arr[low] > arr[mid]) {
                swap(arr, low, mid);
                swaps++;
                recordStep(arr, null,
                        List.of(low, mid), List.of(low, mid), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Median setup: swapping arr[" + low + "] and arr[" + mid + "]");
            }

            if (arr[low] > arr[high]) {
                swap(arr, low, high);
                swaps++;
                recordStep(arr, null,
                        List.of(low, high), List.of(low, high), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Median setup: swapping arr[" + low + "] and arr[" + high + "]");
            }

            if (arr[mid] > arr[high]) {
                swap(arr, mid, high);
                swaps++;
                recordStep(arr, null,
                        List.of(mid, high), List.of(mid, high), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Median setup: swapping arr[" + mid + "] and arr[" + high + "]");
            }
            swap(arr, mid, high);
            swaps++;
            recordStep(arr, high,
                    List.of(), List.of(mid, high), new ArrayList<>(sortedIndices),
                    low, high, depth,
                    "Median value " + arr[high] + " moved to pivot index " + high + ".");
            return arr[high];
        }

        private void swap(int[] arr, int i, int j) {
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }

        private void recordStep(int[] arr, Integer pivotIndex, List<Integer> compareIndices,
                                List<Integer> swapIndices, List<Integer> sortedIndices,
                                int left, int right, int depth, String message) {
            steps.add(new SortStep(
                    arr, pivotIndex, compareIndices, swapIndices, sortedIndices,
                    left, right, depth, comparisons, swaps, message
            ));
        }
    }
}
