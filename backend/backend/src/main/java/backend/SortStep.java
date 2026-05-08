package backend;

import java.util.List;

public class SortStep {
    public int[] array;
    public Integer pivotIndex;
    public List<Integer> compareIndices;
    public List<Integer> swapIndices;
    public List<Integer> sortedIndices;
    public int left;
    public int right;
    public int depth;
    public int comparisons;
    public int swaps;
    public String message;    

    public SortStep(int[] array, Integer pivotIndex, List<Integer> compareIndices,
        List<Integer> swapIndices, List<Integer> sortedIndices, 
        int left, int right, int depth, int comparisons, int swaps, String message){
            this.array = array.clone();
            this.pivotIndex = pivotIndex;  
            this.compareIndices = compareIndices;
            this.swapIndices = swapIndices;
            this.sortedIndices = sortedIndices;
            this.left = left;
            this.right = right;
            this.depth = depth;
            this.comparisons = comparisons;
            this.swaps = swaps;
            this.message = message;
        }
}

