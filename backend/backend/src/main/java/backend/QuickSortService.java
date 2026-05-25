package backend;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Service
public class QuickSortService {
    public SortResponse sort(List<Integer> input) {
        return new SortRun().execute(input);
    }

    private static final class SortRun {
        private final List<SortStep> steps = new ArrayList<>();
        private int comparisons = 0;
        private int swaps = 0;
        private int maxDepth = 0;
        private final Set<Integer> sortedIndices = new HashSet<>();

        SortResponse execute(List<Integer> input) {
            int[] arr = input.stream().mapToInt(Integer::intValue).toArray();
            quickSort(arr, 0, arr.length - 1, 0);
            return new SortResponse(steps, comparisons, swaps, maxDepth);
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

            recordStep(arr, pivotIdx,
                    List.of(), List.of(), new ArrayList<>(sortedIndices),
                    low, high, depth,
                    "Hoare Partition: Starting with pivot " + pivotValue + ". Scanning from both ends.");

            int left = low - 1;
            int right = high + 1;

            while (true) {
                do {
                    left++;
                    comparisons++;
                    recordStep(arr, pivotIdx,
                            List.of(left), List.of(), new ArrayList<>(sortedIndices),
                            low, high, depth,
                            "Hoare Partition: Left pointer scanning → " + arr[left] + (arr[left] < pivotValue ? " < " : " ≥ ") + pivotValue + (arr[left] < pivotValue ? ", keep moving right." : ", STOP."));
                } while (arr[left] < pivotValue);

                do {
                    right--;
                    comparisons++;
                    recordStep(arr, pivotIdx,
                            List.of(right), List.of(), new ArrayList<>(sortedIndices),
                            low, high, depth,
                            "Hoare Partition: Right pointer scanning → " + arr[right] + (arr[right] > pivotValue ? " > " : " ≤ ") + pivotValue + (arr[right] > pivotValue ? ", keep moving left." : ", STOP."));
                } while (arr[right] > pivotValue);

                if (left >= right) {
                    recordStep(arr, pivotIdx,
                            List.of(), List.of(), new ArrayList<>(sortedIndices),
                            low, high, depth,
                            "Hoare Partition: Pointers crossed! Split at index " + right
                                    + " → left subarray [" + low + ".." + right + "], right subarray [" + (right + 1) + ".." + high + "].");
                    return right;
                }

                swap(arr, left, right);
                swaps++;

                if (pivotIdx == left) pivotIdx = right;
                else if (pivotIdx == right) pivotIdx = left;

                recordStep(arr, pivotIdx,
                        List.of(), List.of(left, right), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Hoare Partition: " + arr[left] + " and " + arr[right] + " are on the wrong sides → swapped.");
            }
        }

        private int medianOfThree(int[] arr, int low, int high, int depth) {
            int mid = (low + high) / 2;

            recordStep(arr, null,
                    List.of(), List.of(), new ArrayList<>(sortedIndices),
                    low, high, depth,
                    "Median-of-Three: Finding pivot from first (" + arr[low] + "), middle (" + arr[mid] + "), and last (" + arr[high] + ") elements.");

            comparisons++;
            recordStep(arr, null,
                    List.of(low, mid), List.of(), new ArrayList<>(sortedIndices),
                    low, high, depth,
                    "Median-of-Three: Comparing first (" + arr[low] + ") and middle (" + arr[mid] + ").");
            if (arr[low] > arr[mid]) {
                swap(arr, low, mid);
                swaps++;
                recordStep(arr, null,
                        List.of(low, mid), List.of(low, mid), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Median-of-Three: " + arr[mid] + " > " + arr[low] + " → swapped first and middle.");
            } else {
                recordStep(arr, null,
                        List.of(low, mid), List.of(), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Median-of-Three: " + arr[low] + " ≤ " + arr[mid] + " → no swap needed.");
            }

            comparisons++;
            recordStep(arr, null,
                    List.of(low, high), List.of(), new ArrayList<>(sortedIndices),
                    low, high, depth,
                    "Median-of-Three: Comparing first (" + arr[low] + ") and last (" + arr[high] + ").");
            if (arr[low] > arr[high]) {
                swap(arr, low, high);
                swaps++;
                recordStep(arr, null,
                        List.of(low, high), List.of(low, high), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Median-of-Three: " + arr[high] + " > " + arr[low] + " → swapped first and last.");
            } else {
                recordStep(arr, null,
                        List.of(low, high), List.of(), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Median-of-Three: " + arr[low] + " ≤ " + arr[high] + " → no swap needed.");
            }

            comparisons++;
            recordStep(arr, null,
                    List.of(mid, high), List.of(), new ArrayList<>(sortedIndices),
                    low, high, depth,
                    "Median-of-Three: Comparing middle (" + arr[mid] + ") and last (" + arr[high] + ").");
            if (arr[mid] > arr[high]) {
                swap(arr, mid, high);
                swaps++;
                recordStep(arr, null,
                        List.of(mid, high), List.of(mid, high), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Median-of-Three: " + arr[high] + " > " + arr[mid] + " → swapped middle and last.");
            } else {
                recordStep(arr, null,
                        List.of(mid, high), List.of(), new ArrayList<>(sortedIndices),
                        low, high, depth,
                        "Median-of-Three: " + arr[mid] + " ≤ " + arr[high] + " → no swap needed.");
            }

            swap(arr, mid, high);
            swaps++;
            recordStep(arr, high,
                    List.of(), List.of(mid, high), new ArrayList<>(sortedIndices),
                    low, high, depth,
                    "Median-of-Three: Pivot selected → " + arr[high] + " moved to end (index " + high + ").");
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