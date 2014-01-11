#include <stdio.h>
#include <sndfile.h>

int main() {
   SNDFILE *read_music, *write_music;
   SF_INFO *sfinfo;

   if ((read_music = sf_open("SomeFile.wav", SFM_READ, &sfinfo)) == NULL) {
      printf("read_music: %s\n", sf_sterror(read_music));
      exit(EXIT_FAILURE);
   }

   if ((write_music = sf_open("OutFile.wav", SFM_WRITE, &sfinfo)) == NULL) {
      printf("write_music: %s\n", sf_sterror(write_music));
      exit(EXIT_FAILURE);
   }

   sf_close(read_music);
   sf_close(write_music);
}
