// picoclock.cpp
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "pico/stdlib.h"
#include "pico/rand.h"
// #include "hardware/rtc.h" // Removed RTC include
#include "pico_unicorn.hpp"

using namespace pimoroni;

// Global PicoUnicorn instance
PicoUnicorn pico_unicorn;

const int WIDTH = PicoUnicorn::WIDTH; // 17
const int HEIGHT = PicoUnicorn::HEIGHT; // 7

// Compact 3x7 font data (similar to Python version)
// Using a simple array lookup based on ASCII value
// Store 3 bytes (columns) per char. Index: char - '0' for digits, 10 for ':'
// Max 11 characters needed (0-9, :)
uint8_t compact_font[][3] = {
    {0x7E, 0x42, 0x7E}, // 0: ###  #..# ###
    {0x00, 0x7E, 0x00}, // 1: ...  ###  ...
    {0x7A, 0x4A, 0x4E}, // 2: ##.# #.#. .###
    {0x4A, 0x4A, 0x7E}, // 3: #.#. #.#. ###
    {0x5E, 0x10, 0x7E}, // 4: ###. ..#. ###
    {0x4E, 0x4A, 0x7A}, // 5: .### #.#. ##.#
    {0x7E, 0x4A, 0x7A}, // 6: ###  #.#. ##.#
    {0x42, 0x42, 0x7E}, // 7: #..# #..# ###
    {0x7E, 0x4A, 0x7E}, // 8: ###  #.#. ###
    {0x5E, 0x4A, 0x7E}, // 9: ###. #.#. ###
    {0x00, 0x14, 0x00}  // : (Index 10) - New: Dots at 3rd & 5th position (bits 2 & 4)
};
const int FONT_WIDTH_DIGIT = 3;
const int FONT_WIDTH_COLON = 1; // We draw the colon using only the middle byte above

// Function to display a single character
// Returns the width of the character drawn (including spacing pixels it might occupy)
int display_char(char c, int x_offset, int y_offset, uint8_t r, uint8_t g, uint8_t b) {
    int char_width = 0;
    const uint8_t* font_data = nullptr;

    if (c >= '0' && c <= '9') {
        font_data = compact_font[c - '0'];
        char_width = FONT_WIDTH_DIGIT;
    } else if (c == ':') {
        font_data = compact_font[10]; // Use index 10 for colon
        char_width = FONT_WIDTH_COLON;
    } else {
        return 0; // Character not found
    }

    for (int col = 0; col < char_width; ++col) {
        // Special handling for colon - only draw the middle column data
        int data_col_idx = (c == ':') ? 1 : col;
        uint8_t col_data = font_data[data_col_idx];

        for (int row = 0; row < HEIGHT; ++row) {
            if ((col_data >> row) & 1) {
                pico_unicorn.set_pixel(x_offset + col, y_offset + row, r, g, b);
            }
        }
    }
    return char_width;
}

// Function to display the time string
void display_time_string(const char* time_str, uint8_t r, uint8_t g, uint8_t b) {
    pico_unicorn.clear(); // Clear display buffer

    int current_x = 0; // Start drawing back at column 0
    const int spacing = 1;

    // Restored format: H H :M M -> 3+1+3 + 1 + 3+1+3 = 16
    // H H : M M  => 3 + 1 + 3 + 1 + 1 + 3 + 1 + 3 = 16
    // W S W S W W S W  <-- No, this doesn't match the code below
    // Code logic: Add space after char unless char is ':' or last char.
    // H -> Add Space
    // H -> Add Space
    // : -> NO Space
    // M -> Add Space
    // M -> NO Space (last char)
    // Result: D Sp D Sp : D Sp D = 3+1+3+1+1+3+1+3 = 16 pixels.
    for (int i = 0; time_str[i] != '\0'; ++i) {
        if (current_x >= WIDTH) break; // Don't draw off screen

        char c = time_str[i];
        int char_width = display_char(c, current_x, 0, r, g, b); // y_offset = 0

        current_x += char_width;

        /* // Logic from last attempt (HH:MM - 14/15 pixels)
        // Add spacing only after the second digit (index 1)
        // No space after first digit (index 0)
        // No space after colon (index 2)
        // No space after third digit (index 3)
        // No space after fourth digit (index 4 - end of string)
        if (i == 1 && current_x < WIDTH) { // Add 1 pixel space after HH
             current_x += spacing;
        } else if (c == ':' && current_x < WIDTH) { // Add 1 pixel space after colon
             current_x += spacing;
        }
        */

        // Restored logic: Add space after char unless it is ':' or the last char.
        if (c != ':' && time_str[i+1] != '\0' && current_x < WIDTH) {
             current_x += spacing;
        }
    }
    // pico_unicorn.update() is called implicitly by set_pixel in the C++ lib
}

int main() {
    stdio_init_all(); // Initialize USB serial communication
    pico_unicorn.init();

    // Remove RTC initialization
    // printf("Initializing RTC...\n");
    // rtc_init();
    // sleep_ms(100);

    // Seed random number generator ONCE
    printf("Seeding random number generator...\n");
    srand(get_rand_32());

    // Remove RTC check
    /*
    datetime_t check_dt;
    while (!rtc_running() || !rtc_get_datetime(&check_dt)) {
        printf("Waiting for RTC to start...\n");
        sleep_ms(1000);
    }
    printf("RTC started. Initial time: %04d-%02d-%02d %02d:%02d:%02d\n", 
           check_dt.year, check_dt.month, check_dt.day, 
           check_dt.hour, check_dt.min, check_dt.sec);
    */

    // Initialize time counters
    int current_hour = 6;
    int current_minute = 15;

    printf("Pico Unicorn Clock C++ Version Starting Loop (Counter Mode)...\n");

    while (true) {
        // Get random colors (scale rand() output to 0-255 range)
        uint8_t r = (uint8_t)(rand() % 51 + 20); // 20-70 range approx
        uint8_t g = (uint8_t)(rand() % 51 + 20);
        uint8_t b = (uint8_t)(rand() % 51 + 20);

        // Remove RTC reading
        /*
        datetime_t dt;
        if (!rtc_get_datetime(&dt)) {
             printf("Error getting RTC time!\n");
             // Clear screen on error and wait before retrying
             pico_unicorn.clear();
             sleep_ms(1000);
             continue;
        }
        */

        // Format the time string HH:MM using counters
        char timestring[6]; // HH:MM + null terminator
        snprintf(timestring, sizeof(timestring), "%02d:%02d", current_hour, current_minute);

        printf("Displaying: %s with R=%d, G=%d, B=%d\n", timestring, r, g, b); // Debug print via USB Serial

        // Display the time
        display_time_string(timestring, r, g, b);

        // Wait for 60 seconds
        printf("Sleeping for 60 seconds...\n");
        sleep_ms(60000);

        // Increment time
        current_minute++;
        if (current_minute >= 60) {
            current_minute = 0;
            current_hour++;
            if (current_hour >= 13) { // Rollover from 12 to 1
                current_hour = 1;
            }
        }
    }

    return 0;
} 