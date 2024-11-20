package morkato.api.infra.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;

@Service
public class MorkatoFileBukkit {
  private String path;
  private final Path WORK_DIR;
  private final Path IMAGE_CONTEXT_NAME;
  MorkatoFileBukkit(
    @Autowired Environment env
  ) {
    path = env.getProperty("morkato.workspace.directory", "/usr/morkato");
    WORK_DIR = Paths.get(path);
    IMAGE_CONTEXT_NAME = Paths.get(WORK_DIR.toString(), "image");
  }
  private void ensureDirectoriesExist() throws IOException {
    if (!Files.exists(WORK_DIR)) {
      Files.createDirectories(WORK_DIR);
      Files.createDirectories(IMAGE_CONTEXT_NAME);
    }
    if (!Files.exists(IMAGE_CONTEXT_NAME)) {
      Files.createDirectories(IMAGE_CONTEXT_NAME);
    }
  }
  public String saveImage(byte[] image) throws IOException {
    ensureDirectoriesExist();
    UUID uuid = UUID.randomUUID();
    String filename = uuid + ".bin";
    Path path = Paths.get(IMAGE_CONTEXT_NAME.toString(), filename);
    Files.write(path, image);
    return uuid.toString();
  }
  public InputStream getImage(String uuid) throws IOException {
    Path filename = Paths.get(IMAGE_CONTEXT_NAME.toString(), uuid + ".bin");
    return new FileInputStream(filename.toString());
  }
}
