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
    {0x7F, 0x41, 0x7F}, // 0: 01111111 01000001 01111111 (complete oval)
    {0x00, 0x00, 0x7F}, // 1: 00000000 00000000 01111111 (right vertical line)
    {0x4F, 0x49, 0x79}, // 2: 01001111 01001001 01111001 (proper 2 shape)
    {0x41, 0x49, 0x7F}, // 3: 01000001 01001001 01111111 (proper 3 shape)
    {0x78, 0x08, 0x7F}, // 4: 01111000 00001000 01111111 (proper 4 shape)
    {0x79, 0x49, 0x4F}, // 5: 01111001 01001001 01001111 (proper 5 shape)
    {0x7F, 0x49, 0x4F}, // 6: 01111111 01001001 01001111 (proper 6 shape)
    {0x40, 0x40, 0x7F}, // 7: 01000000 01000000 01111111 (corrected 7 shape)
    {0x7F, 0x49, 0x7F}, // 8: 01111111 01001001 01111111 (proper 8 shape)
    {0x79, 0x49, 0x7F}, // 9: 01111001 01001001 01111111 (proper 9 shape)
    {0x00, 0x24, 0x00}  // : (Index 10): 00000000 00100100 00000000 (2 dots)
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

        // Use all 7 pixels of height
        const int DIGIT_HEIGHT = 7;
        
        for (int row = 0; row < DIGIT_HEIGHT && row < HEIGHT; ++row) {
            // Flip bits vertically during display - bit 0 maps to position 6, etc.
            int bit_position = DIGIT_HEIGHT - 1 - row;
            
            if ((col_data >> bit_position) & 1) {
                // Add +1 to y_offset to shift everything down by one pixel
                pico_unicorn.set_pixel(x_offset + col, y_offset + row + 0, r, g, b);
            }
        }
    }
    return char_width;
}

// Function to display the time string
void display_time_string(const char* time_str, uint8_t r, uint8_t g, uint8_t b) {
    pico_unicorn.clear(); // Clear display buffer

    // Center alignment calculation
    int total_width = 0;
    for (int i = 0; time_str[i] != '\0'; ++i) {
        if (time_str[i] >= '0' && time_str[i] <= '9') {
            total_width += FONT_WIDTH_DIGIT;
        } else if (time_str[i] == ':') {
            total_width += FONT_WIDTH_COLON;
        }
        
        // Add spacing after each character except the last one and colon
        if (time_str[i+1] != '\0' && time_str[i] != ':') {
            total_width += 1; // spacing
        }
    }
    
    // Calculate starting position to center the time
    int start_x = (WIDTH - total_width) / 2;
    if (start_x < 0) start_x = 0;
    
    int current_x = start_x;
    const int spacing = 1;

    for (int i = 0; time_str[i] != '\0'; ++i) {
        if (current_x >= WIDTH) break; // Don't draw off screen

        char c = time_str[i];
        int char_width = display_char(c, current_x, 0, r, g, b); // y_offset = 0

        current_x += char_width;

        // Add space after char unless it is ':' or the last char
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
    int current_hour = 10;
    int current_minute = 03;

    printf("Pico Unicorn Clock C++ Version Starting Loop (Counter Mode)...\n");

    while (true) {
        // Get random colors (scale rand() output to 0-255 range)
        uint8_t r = (uint8_t)(rand() % 11 + 5); // 5-15 range (dimmer)
        uint8_t g = (uint8_t)(rand() % 11 + 5); // 5-15 range (dimmer)
        uint8_t b = (uint8_t)(rand() % 11 + 5); // 5-15 range (dimmer)

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
        // Always use 2 digits for hours (consistent formatting)
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