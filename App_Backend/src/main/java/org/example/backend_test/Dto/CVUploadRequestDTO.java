package org.example.backend_test.Dto;


public class CVUploadRequestDTO {

    private String username;
    private String usermail;
    private Long postid;
    private String postname;
    private String fileName;
    private String fileType;
    private long fileSize;

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getUsermail() {
        return usermail;
    }

    public void setUsermail(String usermail) {
        this.usermail = usermail;
    }

    public Long getPostid() {
        return postid;
    }

    public void setPostid(Long postid) {
        postid = postid;
    }

    public String getPostname() {
        return postname;
    }

    public void setPostname(String postname) {
        postname = postname;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getFileType() {
        return fileType;
    }

    public void setFileType(String fileType) {
        this.fileType = fileType;
    }

    public long getFileSize() {
        return fileSize;
    }

    public void setFileSize(long fileSize) {
        this.fileSize = fileSize;
    }
}
