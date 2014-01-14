/*
 * Tyler Saadus (tsaadus)
 * CSC 344 - Winter 2014
 *
 * Project #1
 * Simple audio rearranger that cuts up an input file and mixes it up
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <sndfile.h>

#define BUFF_LEN 512
#define SAMPLE_LENGTH 2 /* Length, in seconds, of each sample */
#define SWAP_COUNT 30 /*Number of swaps to use in the shuffle function*/

void shuffle(int *array, int len);

int main(int argc, char **argv) {
   SNDFILE *read_music, *write_music;
   SF_INFO sfinfo;
   int data_read;
   int framerate; /* How many 'frames' of data there are in a second */
   int samples[] = {18, 28, 48, 52, 64, 96, 105, 141, 195, 224, 242}; /* Where to sample from in the song */
   uint64_t total_count = 0;
   int* temp_buff;
   int i;
   int num_samples = sizeof(samples)/sizeof(int);

   /* Seed with current time */
   srand(time(NULL));

   /* Make sure that we have input and ouput files specified */
   if (argc != 3) {
      printf("Usage: %s <Input File> <Output File>\n", argv[0]);
      exit(EXIT_FAILURE);
   }

   /* Open input file for reading */
   if ((read_music = sf_open(argv[1], SFM_READ, &sfinfo)) == NULL) {
      printf("%s: %s\n", argv[1], sf_strerror(read_music));
      exit(EXIT_FAILURE);
   }

   /* Open output file for writing */
   if ((write_music = sf_open(argv[2], SFM_WRITE, &sfinfo)) == NULL) {
      printf("%s: %s\n", argv[2], sf_strerror(write_music));
      sf_close(read_music);
      exit(EXIT_FAILURE);
   }

   /* Calculate how many frames there are per second, for seeking purposes */
   framerate = sfinfo.samplerate * sfinfo.channels;

   /* Set up a buffer to hold our samples as we read and write them */
   temp_buff = malloc(framerate*SAMPLE_LENGTH*sizeof(int));

   /* Put our list of samples in a random order */
   shuffle(samples, num_samples);
   printf("Sample order: {");

   /* Seek to the samples in order, read them in and write them to the output*/
   for (i = 0; i < num_samples; i++) {
      if (i == 0) {
         printf("%d", samples[i]);
      } else {
         printf(", %d", samples[i]);
      }

      sf_seek(read_music, framerate*samples[i], SEEK_SET);
      data_read = sf_read_int(read_music, temp_buff, framerate*SAMPLE_LENGTH);
      sf_write_int(write_music, temp_buff, data_read);
      total_count += data_read;
   }
   printf("}\nOutput: %lf seconds\n", (double)total_count / (double)framerate);

   /* Clean up */
   sf_close(read_music);
   sf_close(write_music);
   free(temp_buff);

   return EXIT_SUCCESS;
}

/*
 * Shuffles an arrays contents by swapping two random elements many times
 * Randomizer should be seeded before calling
 */
void shuffle(int *array, int len) {
   int i;
   int a, b, temp;

   for (i = 0; i < SWAP_COUNT; i++) {
      a = rand()%len;
      b = rand()%len;
      temp = array[a];
      array[a] = array[b];
      array[b] = temp;
   }
}
