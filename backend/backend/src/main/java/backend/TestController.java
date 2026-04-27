package backend;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestParam;
import java.util.Map;

@RestController
@CrossOrigin
public class TestController {

    @GetMapping("/api/status")
    public Map<String, String> status(@RequestParam(defaultValue = "Guest") String name) {
        // This is where your heavy Java logic lives
        String processedName = name.toUpperCase().trim();

        return Map.of("message", "Hello " + processedName + "Tangina mo Dean Kubit");
    }
}