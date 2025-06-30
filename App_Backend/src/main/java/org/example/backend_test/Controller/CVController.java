package org.example.backend_test.Controller;

import org.example.backend_test.Service.CvDocumentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/cv")
public class CVController {

    //private final CVDocumentRepository cvDocumentRepository;
    @Autowired
    private  CvDocumentService cvDocumentService;

//    //public CVController(CVDocumentRepository cvDocumentRepository) {
//        this.cvDocumentRepository = cvDocumentRepository;
//    }

    @PostMapping("/upload")
    public ResponseEntity<String> uploadCV(
            @RequestParam("file") MultipartFile file,
            @RequestParam("username") String username,
            @RequestParam("usermail") String usermail,
            @RequestParam("postname") String postname,
            @RequestParam("postid") String postid
    ) {
        try {
            // Process file
            String path = "/home/imed/Bureau/Backend_Test/src/main/java/org/example/backend_test/localcv";
            File destination = new File(path, file.getOriginalFilename());
            file.transferTo(destination);

            // Optional: Save metadata or log it
            System.out.println("Uploaded by: " + username + ", " + usermail);
            System.out.println("Post: " + postname + ", ID: " + postid);

            return ResponseEntity.ok("CV uploaded successfully.");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Upload failed: " + e.getMessage());
        }
    }
    @GetMapping("/scores")
    public ResponseEntity<Map<String, Object>> getScores() {
        try {
            Map<String, Object> response = new HashMap<>();

            Map<String, Object> customScore = new HashMap<>();
            customScore.put("total_score", 75);
            customScore.put("detailed_scores", Map.of(
                    "skills", 80,
                    "experience", 70,
                    "education", 75
            ));
            customScore.put("experience_metrics", Map.of(
                    "details", "3 years experience in Angular, Java"
            ));
            customScore.put("feedback", List.of("Good skills", "Needs improvement in backend"));

            List<String> recommendations = List.of(
                    "Learn advanced TypeScript",
                    "Improve backend Java skills"
            );

            response.put("custom", customScore);
            response.put("recommendations", recommendations);

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }
}



//    @GetMapping("/download/{id}")
//    public ResponseEntity<byte[]> downloadCV(@PathVariable Long id) {
//        CVDocument document = cvDocumentRepository.findById(id)
//                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "CV document not found"));
//
//        HttpHeaders headers = new HttpHeaders();
//        headers.setContentType(MediaType.APPLICATION_PDF);
//        headers.setContentDispositionFormData("attachment", document.getFileName());
//        headers.setContentLength(document.getFileSize());
//
//        return new ResponseEntity<>(document.getFileData(), headers, HttpStatus.OK);
//    }
