package backend;

import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;

@RestController
@CrossOrigin(origins = "*")
public class SortController {

    private final QuickSortService sortService;

    public SortController(QuickSortService sortService) {
        this.sortService = sortService;
    }

    @PostMapping("/sort")
    public SortResponse sort(@RequestBody SortRequest req) {
        if (req == null || req.array == null || req.array.isEmpty()) {
            throw new IllegalArgumentException("Array must not be empty.");
        }
        if (req.array.size() > 500) {
            throw new IllegalArgumentException("Array size must be at most 500 (step trace limit).");
        }
        return sortService.sort(req.array);
    }

    @GetMapping("/array/random")
    public List<Integer> randomArray(
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "1")  int min,
            @RequestParam(defaultValue = "99") int max) {

        if (size < 0) {
            throw new IllegalArgumentException("size must be non-negative.");
        }
        if (size > 500) {
            throw new IllegalArgumentException("size must be at most 500.");
        }
        if (min > max) {
            throw new IllegalArgumentException("min must be less than or equal to max.");
        }
        Random rng = new Random();
        List<Integer> result = new ArrayList<>();
        int span = max - min + 1;
        for (int i = 0; i < size; i++) {
            result.add(rng.nextInt(span) + min);
        }
        return result;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "UP");
    }
}