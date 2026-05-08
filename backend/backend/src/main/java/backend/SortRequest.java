package backend;

import java.util.List;
public class SortRequest {
    public List<Integer> array;
    public String pivot;

    public SortRequest() {}

    public SortRequest(List<Integer> array, String pivot){
        this.array = array;
        this.pivot = pivot;
    }
}
