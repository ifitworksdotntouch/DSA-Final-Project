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
        if (req.array == null || req.array.isEmpty()) {
            throw new IllegalArgumentException("Array must not be empty.");
        }
        return sortService.sort(req.array);
    }

    @GetMapping("/array/random")
    public List<Integer> randomArray(
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "1")  int min,
            @RequestParam(defaultValue = "99") int max) {

        Random rng = new Random();
        List<Integer> result = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            result.add(rng.nextInt(max - min + 1) + min);
        }
        return result;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "UP");
    }
}