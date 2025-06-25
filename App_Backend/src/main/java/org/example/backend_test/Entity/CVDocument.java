package org.example.backend_test.Entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "cv_documents")
public class CVDocument {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String username;

    @Column(nullable = false)
    private String usermail;

    @Column(nullable = false)
    private Long postid;

    @Column(nullable = false)
    private String postname;

    @Column(nullable = false)
    private String fileName;

    @Column(nullable = false)
    private String fileType;

    @Column(nullable = false)
    private Long fileSize;

    @Lob
    @Column(name = "file_data", columnDefinition = "LONGBLOB")
    private byte[] fileData;

    @Column(nullable = false)
    private LocalDateTime uploadedAt;
    public CVDocument(String username, String usermail, String postname, Long postid,
                      String fileName, String fileType, long fileSize, byte[] fileData) {
        this.username = username;
        this.usermail = usermail;
        this.postname = postname;
        this.postid = postid;
        this.fileName = fileName;
        this.fileType = fileType;
        this.fileSize = fileSize;
        this.fileData = fileData;
    }
}