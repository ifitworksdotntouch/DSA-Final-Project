package backend;

import java.util.List;

public class SortResponse {
    public List<SortStep> steps;
    public int totalComparisons;
    public int totalSwaps;
    public int maxDepth;   

    public SortResponse(List<SortStep> steps, 
        int totalComparisons, 
        int totalSwaps, int maxDepth){

        this.steps = steps;
        this.totalComparisons = totalComparisons;
        this.totalSwaps = totalSwaps;
        this.maxDepth = maxDepth;
    }
}
