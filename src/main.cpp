/* Copyright (c) Nikolaj Goodger */

#include <pybind11/cast.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <stdio.h>
#include <unistd.h>

#include <array>
#include <cassert>
#include <cstring>
#include <deque>
#include <iostream>
#include <list>
#include <map>
#include <memory>
#include <set>
#include <string>
#include <vector>

#include "include/display.h"

// "digit" is declared in both Python's longintrepr.h and NetHack's extern.h.
#define digit nethack_digit

extern "C" {
#include "include/hack.h"
}

namespace py = pybind11;

// Dungeon dimensions
#define DUNGEON_WIDTH 79u
#define DUNGEON_HEIGHT 21u

enum DIRECTION {
  east,
  southeast,
  south,
  southwest,
  west,
  northwest,
  north,
  northeast
};

namespace nle_language_obsv {

class NLELanguageObsv {
 public:
  NLELanguageObsv(void);
  py::bytes text_glyphs(py::array_t<int16_t> glyphs,
                        py::array_t<int64_t> blstats);
  py::bytes text_blstats(py::array_t<int64_t> blstats);
  py::bytes text_inventory(py::array_t<uint8_t> inv_strs,
                           py::array_t<uint8_t> inv_letters);
  py::bytes text_cursor(py::array_t<int16_t> glyphs,
                        py::array_t<int64_t> blstats,
                        py::array_t<int64_t> tty_cursor);
  py::bytes text_message(py::array_t<uint8_t> tty_chars);

 private:
  const std::set<std::string> cmap_floor{
      "room floor",
      "dark room floor",
      "corridor floor",
      "lit corridor floor",
  };

  const std::set<std::string> blocking_view{
      "dark area",
      "vertical wall",
      "horizontal wall",
      "northwest room corner",
      "northeast room corner",
      "southwest corner",
      "southeast corner",
      "cross wall",
      "t up wall",
      "t down wall",
      "t west wall",
      "t east wall",
      "horizontal closed door",
      "vertical closed door",
      "horizontal raised drawbridge",
      "vertical raised drawbridge",
  };

  const std::set<std::string> cmap_screen_include{
      "horizontal closed door",
      "vertical closed door",
      "bars",
      "tree",
      "stairs up",
      "stairs down",
      "ladder up",
      "ladder down",
      "alter",
      "grave",
      "throne",
      "sink",
      "fountain",
      "pool",
      "ice",
      "lava",
      "vertical raised drawbridge",
      "horizontal raised drawbridge",
  };
  const char *cmap_lookup[100]{
      "dark area",
      "vertical wall",
      "horizontal wall",
      "northwest room corner",
      "northeast room corner",
      "southwest corner",
      "southeast corner",
      "cross wall",
      "t up wall",
      "t down wall",
      "t west wall",
      "t east wall",
      "doorway",
      "vertical open door",
      "horizontal open door",
      "vertical closed door",
      "horizontal closed door",
      "bars",
      "tree",
      "room floor",
      "dark room floor",
      "corridor floor",
      "lit corridor floor",
      "stairs up",
      "stairs down",
      "ladder up",
      "ladder down",
      "alter",
      "grave",
      "throne",
      "sink",
      "fountain",
      "pool",
      "ice",
      "lava",
      "vertical lowered drawbridge",
      "horizontal lowered drawbridge",
      "vertical raised drawbridge",
      "horizontal raised drawbridge",
      "air floor",
      "cloud floor",
      "water floor",
      "arrow trap",
      "dart trap",
      "falling rock trap",
      "squeaky board",
      "bear trap",
      "land mine",
      "rolling boulder trap",
      "sleeping gas trap",
      "rust trap",
      "fire trap",
      "pit",
      "spiked pit",
      "hole",
      "trap door",
      "teleportation trap",
      "level teleporter",
      "magic portal",
      "web",
      "statue trap",
      "magic trap",
      "anti magic trap",
      "polymorph trap",
      "vibrating square",
      "vertical beam",
      "horizontal beam",
      "left slant beam",
      "right slant beam",
      "dig beam",
      "flash beam",
      "boom left",
      "boom right",
      "shield 1",
      "shield 2",
      "shield 3",
      "shield 4",
      "poison cloud",
      "valid position",
      "swallow top left",
      "swallow top center",
      "swallow top right",
      "swallow middle left",
      "swallow middle right",
      "swallow bottom left",
      "swallow bottom center",
      "swallow bottom right",
      "explosion top left",
      "explosion top center",
      "explosion top right",
      "explosion middle left",
      "explosion middle center",
      "explosion middle right",
      "explosion bottom left",
      "explosion bottom center",
      "explosion bottom right",
      "MAXPCHARS",
  };
  std::string Im_unused;
  void build_fullscreen_view_glyph_map();
  std::list<std::tuple<std::string, std::string, std::string>>
  sort_by_distance_direction(
      std::list<std::tuple<std::string, std::string, std::string>>
          glyph_distance_direction);
  std::list<std::tuple<std::string, std::string, std::string>>
  compress_by_glyph(std::list<std::tuple<std::string, std::string, std::string>>
                        glyph_distance_direction_set);
  void build_screen_pos_to_distance_direction(void);
  void build_noun_plural_lookup();
  void build_visual_view_glyph_map();
  std::pair<std::string, std::string> pos_to_str(int x, int y);
  std::string offset_to_str(int offset);
  int diagonal_distance(int dx, int dy);
  std::list<std::tuple<std::string, std::string, std::string>> fullscreen_view(
      int16_t *glyphs_data, int64_t *blstats_data);
  std::list<std::tuple<std::string, std::string, std::string>> visual_view(
      int16_t *glyphs_data, int64_t *blstats_data);
  std::pair<int, int> local_glyph_to_global(int glyph_idx, int player_x,
                                            int player_y);
  std::string trim(std::string input);
  std::list<std::tuple<std::string, std::string, std::string>> ray_march(
      DIRECTION direction, int64_t player_x, int64_t player_y,
      int16_t *glyphs_data);

  std::array<std::string, MAX_GLYPH> fullscreen_view_glyph_map;
  std::array<std::string, MAX_GLYPH> visual_view_glyph_map;
  std::map<std::string, std::string> noun_plural_lookup;
  std::array<
      std::array<std::pair<std::string, std::string>, DUNGEON_HEIGHT * 2>,
      DUNGEON_WIDTH * 2>
      screen_distance_direction_lookup;
  std::string pluralize(std::string noun);
  std::string replace_word(std::string input, std::string word,
                           std::string replacement_word);
};

void NLELanguageObsv::build_screen_pos_to_distance_direction() {
  for (uint64_t x = 0; x < DUNGEON_WIDTH * 2; x++) {
    for (uint64_t y = 0; y < DUNGEON_HEIGHT * 2; y++) {
      screen_distance_direction_lookup[x][y] =
          pos_to_str(x - DUNGEON_WIDTH, y - DUNGEON_HEIGHT);
    }
  }
}

NLELanguageObsv::NLELanguageObsv() {
  // Initialize the lookup tables for glyphs & positions.
  build_fullscreen_view_glyph_map();
  build_visual_view_glyph_map();
  build_screen_pos_to_distance_direction();
  build_noun_plural_lookup();
}

void NLELanguageObsv::build_noun_plural_lookup() {
  for (auto screen_it = fullscreen_view_glyph_map.begin();
       screen_it != fullscreen_view_glyph_map.end(); ++screen_it) {
    noun_plural_lookup[*screen_it] = pluralize(*screen_it);
  }
  for (auto near_it = visual_view_glyph_map.begin();
       near_it != visual_view_glyph_map.end(); ++near_it) {
    noun_plural_lookup[*near_it] = pluralize(*near_it);
  }
}

std::string NLELanguageObsv::pluralize(std::string noun) {
  std::string plural;
  // Mass nouns
  if (noun.size() >= 5 && noun.substr(noun.size() - 5) == "boots")
    plural = noun;
  else if (noun.size() >= 5 && noun.substr(noun.size() - 5) == "shoes")
    plural = noun;
  else if (noun.size() >= 6 && noun.substr(noun.size() - 6) == "scales")
    plural = noun;
  else if (noun.size() >= 6 && noun.substr(noun.size() - 6) == "lenses")
    plural = noun;
  else if (noun.size() >= 4 && noun.substr(noun.size() - 4) == "bars")
    plural = noun;
  // Exceptions.
  else if (noun == "can of grease")
    plural = "cans of grease";
  else if (noun == "Master of Thieves")
    plural = "Masters of Thieves";
  else if (noun == "ice")
    plural = "area of ice";
  else if (noun == "lava")
    plural = "area of lava";
  else if (noun.substr(0, 5) == "boom ")
    plural = noun.replace(0, 5, "booms ");
  else if (noun.substr(0, 7) == "shield ")
    plural = noun.replace(0, 7, "shields ");
  else if (noun.substr(0, 8) == "swallow ")
    plural = noun.replace(0, 8, "swallows ");
  else if (noun.substr(0, 7) == "scroll ")
    plural = noun.replace(0, 7, "scrolls ");
  else if (noun.substr(0, 16) == "worthless piece ")
    plural = noun.replace(0, 16, "worthless pieces ");
  else if (noun.substr(0, 17) == "unknown creature ")
    plural = noun.replace(0, 17, "unknown creatures ");
  // Normal pluralization rules
  else if (noun[noun.size() - 1] == 'y' &&
           !(noun[noun.size() - 2] == 'a' || noun[noun.size() - 2] == 'e' ||
             noun[noun.size() - 2] == 'i' || noun[noun.size() - 2] == 'o' ||
             noun[noun.size() - 2] == 'u')) {
    plural = noun.substr(0, noun.size() - 1) + "ies";
  } else if (noun[noun.size() - 1] == 'z' || noun[noun.size() - 1] == 'x' ||
             (noun[noun.size() - 2] == 'c' && noun[-1] == 'h') ||
             (noun[noun.size() - 2] == 's' && noun[noun.size() - 1] == 'h') ||
             (noun[noun.size() - 2] == 's' && noun[noun.size() - 1] == 's')) {
    plural = noun + "es";
  } else if (noun[noun.size() - 1] == 'f') {
    if (noun[noun.size() - 2] == 'f')
      plural = noun.substr(0, noun.size() - 2) + "ves";
    else
      plural = noun.substr(0, noun.size() - 1) + "ves";
  } else if (noun[noun.size() - 1] == 's') {
    plural = noun + "es";
  } else {
    plural = noun + "s";
  }
  return plural;
}

std::list<std::tuple<std::string, std::string, std::string>>
NLELanguageObsv::compress_by_glyph(
    std::list<std::tuple<std::string, std::string, std::string>>
        glyph_distance_direction) {
  std::list<std::tuple<std::string, std::string, std::string>>
      new_glyph_distance_direction;
  std::vector<std::pair<std::string, std::string>>
      vector_glyh_distance_to_directions;
  std::vector<std::pair<std::string, std::string>>
      new_vector_glyh_distance_to_directions;
  std::map<std::pair<std::string, std::string>, std::vector<std::string>>
      map_glyh_distance_to_directions;

  for (auto it = glyph_distance_direction.begin();
       it != glyph_distance_direction.end(); it++) {
    std::string glyph_string = std::get<0>(*it);
    std::string distance_string = std::get<1>(*it);
    std::string direction_string = std::get<2>(*it);

    std::pair<std::string, std::string> glyph_distance_string_pair =
        std::make_pair(glyph_string, distance_string);
    // We use the vector to retain the sorted order.
    if (map_glyh_distance_to_directions.find(glyph_distance_string_pair) ==
        map_glyh_distance_to_directions.end()) {
      vector_glyh_distance_to_directions.push_back(glyph_distance_string_pair);
    }
    map_glyh_distance_to_directions[glyph_distance_string_pair].push_back(
        direction_string);
  }
  std::map<std::pair<std::string, std::string>, std::vector<std::string>>
      new_map_glyh_distance_to_directions;

  for (auto it = vector_glyh_distance_to_directions.begin();
       it != vector_glyh_distance_to_directions.end(); it++) {
    std::string glyph_string = it->first;
    std::string distance_string = it->second;
    std::vector<std::string> direction_strings =
        map_glyh_distance_to_directions[*it];
    std::map<std::string, int> direction_freq;
    std::vector<std::string> direction_freq_order;
    std::vector<std::string> multiple_in_direction;
    std::vector<std::string> single_direction_strings;

    // For the current glyph & distance check the frequency of each direction.
    for (auto direction_it = direction_strings.begin();
         direction_it != direction_strings.end(); direction_it++) {
      // Use a vector to preserve the order of the directions.
      if (direction_freq.find(*direction_it) == direction_freq.end())
        direction_freq_order.push_back(*direction_it);
      direction_freq[*direction_it]++;
    }

    // For the current glyph & distance check if there is one distance or
    // multiple.
    for (auto direction_freq_it = direction_freq_order.begin();
         direction_freq_it != direction_freq_order.end(); direction_freq_it++) {
      if (direction_freq[*direction_freq_it] == 1)
        single_direction_strings.push_back(*direction_freq_it);
      else
        multiple_in_direction.push_back(*direction_freq_it);
    }

    if (single_direction_strings.size() > 0) {
      new_vector_glyh_distance_to_directions.push_back(*it);
      new_map_glyh_distance_to_directions[*it] = single_direction_strings;
    }
    if (multiple_in_direction.size() > 0) {
      std::pair<std::string, std::string> glyph_distance_string_pair =
          std::make_pair(noun_plural_lookup[glyph_string], distance_string);
      new_vector_glyh_distance_to_directions.push_back(
          glyph_distance_string_pair);
      new_map_glyh_distance_to_directions[glyph_distance_string_pair] =
          multiple_in_direction;
    }
  }
  vector_glyh_distance_to_directions = new_vector_glyh_distance_to_directions;
  map_glyh_distance_to_directions = new_map_glyh_distance_to_directions;

  for (auto it = vector_glyh_distance_to_directions.begin();
       it != vector_glyh_distance_to_directions.end(); ++it) {
    std::string glyph_string = it->first;
    std::string distance_string = it->second;
    std::vector<std::string> direction_strings =
        map_glyh_distance_to_directions[*it];

    if (direction_strings.size() == 1) {
      std::string first_direction = direction_strings[0];
      new_glyph_distance_direction.push_back(
          make_tuple(glyph_string, distance_string, first_direction));
    } else if (direction_strings.size() == 2) {
      std::string first_direction = direction_strings[0];
      std::string second_direction = direction_strings[1];
      std::string new_direction = first_direction + " and " + second_direction;
      new_glyph_distance_direction.push_back(
          make_tuple(glyph_string, distance_string, new_direction));
    } else {
      std::string last_direction =
          direction_strings[direction_strings.size() - 1];
      std::string new_direction = "";
      new_direction += direction_strings[0];
      for (uint64_t i = 1; i < direction_strings.size() - 1; i++) {
        new_direction += ", " + direction_strings[i];
      }
      new_direction += ", and " + last_direction;
      new_glyph_distance_direction.push_back(
          make_tuple(glyph_string, distance_string, new_direction));
    }
  }
  return new_glyph_distance_direction;
}

std::pair<int, int> NLELanguageObsv::local_glyph_to_global(int glyph_idx,
                                                           int player_x,
                                                           int player_y) {
  int glyph_x = glyph_idx % DUNGEON_WIDTH;
  int glyph_y = glyph_idx / DUNGEON_WIDTH;
  int glyph_relative_x = glyph_x - player_x;
  int glyph_relative_y = -glyph_y + player_y;

  int glyph_relative_start_0_x = glyph_relative_x + DUNGEON_WIDTH;
  int glyph_relative_start_0_y = glyph_relative_y + DUNGEON_HEIGHT;

  return std::make_pair(glyph_relative_start_0_x, glyph_relative_start_0_y);
}

std::list<std::tuple<std::string, std::string, std::string>>
NLELanguageObsv::sort_by_distance_direction(
    std::list<std::tuple<std::string, std::string, std::string>>
        glyph_distance_direction) {
  std::list<std::tuple<std::string, std::string, std::string>>
      new_glyph_distance_direction;
  const std::array<std::string, 5> distance_order = {"very far", "far", "near",
                                                     "very near", "adjacent"};
  const std::array<std::string, 16> direction_order = {
      "north", "northnortheast", "northeast", "eastnortheast",
      "east",  "eastsoutheast",  "southeast", "southsoutheast",
      "south", "southsouthwest", "southwest", "westsouthwest",
      "west",  "westnorthwest",  "northwest", "northnorthwest"};

  for (auto distances_it = distance_order.begin();
       distances_it != distance_order.end(); ++distances_it) {
    for (auto directions_it = direction_order.begin();
         directions_it != direction_order.end(); ++directions_it) {
      for (auto it = glyph_distance_direction.begin();
           it != glyph_distance_direction.end(); ++it) {
        std::string distance_string = std::get<1>(*it);
        std::string direction_string = std::get<2>(*it);

        if (distance_string == *distances_it &&
            direction_string == *directions_it) {
          new_glyph_distance_direction.push_back(*it);
        }
      }
    }
  }
  return new_glyph_distance_direction;
}

std::list<std::tuple<std::string, std::string, std::string>>
NLELanguageObsv::ray_march(DIRECTION direction, int64_t player_x,
                           int64_t player_y, int16_t *glyphs_data) {
  std::list<std::tuple<std::string, std::string, std::string>>
      glyph_distance_direction;
  std::string glyph_string;
  std::string direction_string;
  std::string distance_string;

  for (uint64_t offset = 1; offset < 10; offset++) {
    int64_t glyph_x = 0, glyph_y = 0;

    switch (direction) {
      case east:
        glyph_x = player_x + offset;
        glyph_y = player_y;
        break;
      case southeast:
        glyph_x = player_x + offset;
        glyph_y = player_y + offset;
        break;
      case south:
        glyph_x = player_x;
        glyph_y = player_y + offset;
        break;
      case southwest:
        glyph_x = player_x - offset;
        glyph_y = player_y + offset;
        break;
      case west:
        glyph_x = player_x - offset;
        glyph_y = player_y;
        break;
      case northwest:
        glyph_x = player_x - offset;
        glyph_y = player_y - offset;
        break;
      case north:
        glyph_x = player_x;
        glyph_y = player_y - offset;
        break;
      case northeast:
        glyph_x = player_x + offset;
        glyph_y = player_y - offset;
        break;
    }

    // Avoid out of range of range
    if ((glyph_x >= DUNGEON_WIDTH || glyph_x < 0) ||
        (glyph_y >= DUNGEON_HEIGHT || glyph_y < 0))
      break;

    int64_t glyph_idx = glyph_x + glyph_y * DUNGEON_WIDTH;
    auto [glyph_relative_start_0_x, glyph_relative_start_0_y] =
        local_glyph_to_global(glyph_idx, player_x, player_y);

    int glyph = glyphs_data[glyph_idx];
    std::string glyph_value = visual_view_glyph_map[glyph];
    if (fullscreen_view_glyph_map[glyph].size() == 0 &&
        glyph_value.size() > 0) {
      glyph_string = glyph_value;
      direction_string =
          screen_distance_direction_lookup[glyph_relative_start_0_x]
                                          [glyph_relative_start_0_y]
                                              .first;
      distance_string =
          screen_distance_direction_lookup[glyph_relative_start_0_x]
                                          [glyph_relative_start_0_y]
                                              .second;
      glyph_distance_direction.push_back(
          std::make_tuple(glyph_string, direction_string, distance_string));
      if (blocking_view.find(glyph_value) != blocking_view.end()) {
        break;
      }
    }
  }
  return glyph_distance_direction;
}

std::list<std::tuple<std::string, std::string, std::string>>
NLELanguageObsv::fullscreen_view(int16_t *glyphs_data, int64_t *blstats_data) {
  int64_t player_x = blstats_data[0];
  int64_t player_y = blstats_data[1];

  std::list<std::tuple<std::string, std::string, std::string>>
      glyph_distance_direction;
  std::string glyph_string;
  std::string direction_string;
  std::string distance_string;

  int16_t glyph;
  int64_t glyph_relative_start_0_x;
  int64_t glyph_relative_start_0_y;

  int64_t glyph_x;
  int64_t glyph_y;
  for (int64_t i = 0; i < DUNGEON_WIDTH * DUNGEON_HEIGHT; i++) {
    glyph = glyphs_data[i];
    std::string glyph_value = fullscreen_view_glyph_map[glyph];

    if (glyph_value.size() > 0) {
      glyph_x = i % DUNGEON_WIDTH;
      glyph_y = i / DUNGEON_WIDTH;
      int glyph_relative_x = glyph_x - player_x;
      int glyph_relative_y = -glyph_y + player_y;

      // Skip player
      if (glyph_relative_x == 0 && glyph_relative_y == 0) continue;

      glyph_string = glyph_value;

      glyph_relative_start_0_x = glyph_relative_x + DUNGEON_WIDTH;
      glyph_relative_start_0_y = glyph_relative_y + DUNGEON_HEIGHT;

      distance_string =
          screen_distance_direction_lookup[glyph_relative_start_0_x]
                                          [glyph_relative_start_0_y]
                                              .first;
      direction_string =
          screen_distance_direction_lookup[glyph_relative_start_0_x]
                                          [glyph_relative_start_0_y]
                                              .second;
      glyph_distance_direction.push_back(
          std::make_tuple(glyph_string, distance_string, direction_string));
    }
  }
  return glyph_distance_direction;
}

std::list<std::tuple<std::string, std::string, std::string>>
NLELanguageObsv::visual_view(int16_t *glyphs_data, int64_t *blstats_data) {
  int64_t player_x = blstats_data[0];
  int64_t player_y = blstats_data[1];

  std::list<std::tuple<std::string, std::string, std::string>>
      glyph_distance_direction;
  std::string glyph_string;
  std::string direction_string;
  std::string distance_string;

  std::vector<DIRECTION> directions = {east, southeast, south, southwest,
                                       west, northwest, north, northeast};

  for (auto it = directions.begin(); it != directions.end(); ++it) {
    glyph_distance_direction.splice(
        glyph_distance_direction.end(),
        ray_march(*it, player_x, player_y, glyphs_data));
  }
  return glyph_distance_direction;
}

void NLELanguageObsv::build_visual_view_glyph_map() {
  for (int16_t glyph = 0; glyph < MAX_GLYPH; glyph++) {
    if (glyph >= GLYPH_CMAP_OFF && glyph < GLYPH_EXPLODE_OFF) { /* cmap */
      std::string cmap_str = cmap_lookup[glyph_to_cmap(glyph)];
      bool is_not_floor = cmap_floor.find(cmap_str) == cmap_floor.end();
      bool is_not_included_in_fullscreen_view =
          cmap_screen_include.find(cmap_str) == cmap_screen_include.end();
      if (is_not_floor && is_not_included_in_fullscreen_view) {
        visual_view_glyph_map[glyph] = cmap_str;
      } else {
        visual_view_glyph_map[glyph] = "";
      }
    } else
      visual_view_glyph_map[glyph] = "";
  }
}

void NLELanguageObsv::build_fullscreen_view_glyph_map() {
  for (int16_t glyph = 0; glyph < MAX_GLYPH; glyph++) {
    if (glyph >= GLYPH_STATUE_OFF) {
      struct permonst *monster = &mons[glyph_to_mon(glyph)];
      fullscreen_view_glyph_map[glyph] =
          +monster->mname + std::string(" statue");
    } else if (glyph >= GLYPH_WARNING_OFF) {
      int warnindx = glyph_to_warning(glyph);
      fullscreen_view_glyph_map[glyph] =
          std::string(def_warnsyms[warnindx].explanation);
    } else if (glyph >= GLYPH_SWALLOW_OFF) {
      static const std::array<std::string, 8> swallow_names = {
          "swallow top left",      "swallow top center",
          "swallow top right",     "swallow middle left",
          "swallow middle right",  "swallow bottom left",
          "swallow bottom center", "swallow bottom right",
      };
      int64_t swallow_idx = (glyph - GLYPH_SWALLOW_OFF) % swallow_names.size();
      fullscreen_view_glyph_map[glyph] = swallow_names[swallow_idx];
    } else if (glyph >= GLYPH_ZAP_OFF) {
      static const std::array<std::string, 4> zap_beam_names = {
          "horizontal zap beam", "vertical zap beam", "left slant zap beam",
          "right slant zap beam"};
      int64_t beam_idx = (glyph - GLYPH_ZAP_OFF) % zap_beam_names.size();
      fullscreen_view_glyph_map[glyph] = zap_beam_names[beam_idx];

    } else if (glyph >= GLYPH_EXPLODE_OFF) {
      static const std::array<std::string, MAXEXPCHARS> explosion_names = {
          "explosion top left",      "explosion top center",
          "explosion top right",     "explosion middle left",
          "explosion middle center", "explosion middle right",
          "explosion bottom left",   "explosion bottom center",
          "explosion bottom right",
      };
      int idx = ((glyph - GLYPH_EXPLODE_OFF) % MAXEXPCHARS);
      fullscreen_view_glyph_map[glyph] = explosion_names[idx];
    } else if (glyph >= GLYPH_CMAP_OFF) {
      std::string cmap_str = cmap_lookup[glyph_to_cmap(glyph)];
      bool is_not_floor = cmap_floor.find(cmap_str) == cmap_floor.end();
      bool should_include =
          cmap_screen_include.find(cmap_str) != cmap_screen_include.end();
      if (is_not_floor && should_include)
        fullscreen_view_glyph_map[glyph] = cmap_str;
      else
        fullscreen_view_glyph_map[glyph] = "";
    } else if (glyph >= GLYPH_OBJ_OFF) {
      std::string obj_name, obj_description;
      char obj_class = objects[glyph_to_obj(glyph)].oc_class;

      if (obj_descr[glyph_to_obj(glyph)].oc_name != NULL)
        obj_name = std::string(obj_descr[glyph_to_obj(glyph)].oc_name);
      else
        obj_name = "";

      if (obj_descr[glyph_to_obj(glyph)].oc_descr != NULL)
        obj_description = std::string(obj_descr[glyph_to_obj(glyph)].oc_descr);
      else
        obj_description = "";

      switch (obj_class) {
        case ILLOBJ_CLASS:
          fullscreen_view_glyph_map[glyph] = obj_name;
          break;
        case WEAPON_CLASS:
          fullscreen_view_glyph_map[glyph] = obj_name;
          break;
        case ARMOR_CLASS:
          if (obj_description.size() > 0)
            fullscreen_view_glyph_map[glyph] = obj_description;
          else
            fullscreen_view_glyph_map[glyph] = obj_name;
          break;
        case RING_CLASS:
          fullscreen_view_glyph_map[glyph] = obj_description + " ring";
          break;
        case AMULET_CLASS:
          if (obj_description.find("Amulet") == std::string::npos)
            fullscreen_view_glyph_map[glyph] = obj_description + " amulet";
          else
            fullscreen_view_glyph_map[glyph] = obj_description;
          break;
        case TOOL_CLASS:
          if (obj_description.size() > 0)
            fullscreen_view_glyph_map[glyph] = obj_description;
          else
            fullscreen_view_glyph_map[glyph] = obj_name;
          break;
        case FOOD_CLASS:
          fullscreen_view_glyph_map[glyph] = obj_name + obj_description;
          break;
        case POTION_CLASS:
          fullscreen_view_glyph_map[glyph] = obj_description + " potion";
          break;
        case SCROLL_CLASS:
          fullscreen_view_glyph_map[glyph] =
              "scroll labeled " + obj_description;
          break;
        case SPBOOK_CLASS:
          fullscreen_view_glyph_map[glyph] = obj_description + " spellbook";
          break;
        case WAND_CLASS:
          fullscreen_view_glyph_map[glyph] = obj_description + " wand";
          break;
        case COIN_CLASS:
          fullscreen_view_glyph_map[glyph] = obj_name;
          break;
        case GEM_CLASS:
          if (obj_name.find(obj_description) == std::string::npos)
            fullscreen_view_glyph_map[glyph] = obj_description + " " + obj_name;
          else
            fullscreen_view_glyph_map[glyph] = obj_name;
          break;
        case ROCK_CLASS:
          fullscreen_view_glyph_map[glyph] = obj_name;
          break;
        case BALL_CLASS:
          fullscreen_view_glyph_map[glyph] = obj_name;
          break;
        case CHAIN_CLASS:
          fullscreen_view_glyph_map[glyph] = obj_name;
          break;
        case VENOM_CLASS:
          fullscreen_view_glyph_map[glyph] = "splash of " + obj_name;
          break;
        default:
          fullscreen_view_glyph_map[glyph] = "";
          break;
      }
    } else if (glyph >= GLYPH_RIDDEN_OFF) {
      struct permonst *monster = &mons[glyph_to_mon(glyph)];
      fullscreen_view_glyph_map[glyph] =
          std::string("ridden ") + monster->mname;
    } else if (glyph >= GLYPH_BODY_OFF) {
      int64_t monster_idx = glyph - GLYPH_BODY_OFF;
      struct permonst *monster = &mons[monster_idx];
      fullscreen_view_glyph_map[glyph] =
          monster->mname + std::string(" corpse");
    } else if (glyph >= GLYPH_DETECT_OFF) {
      struct permonst *monster = &mons[glyph_to_mon(glyph)];
      fullscreen_view_glyph_map[glyph] =
          std::string("detected ") + monster->mname;
    } else if (glyph >= GLYPH_INVIS_OFF) {
      fullscreen_view_glyph_map[glyph] = "invisible creature";
    } else if (glyph >= GLYPH_PET_OFF) {
      struct permonst *monster = &mons[glyph_to_mon(glyph)];
      fullscreen_view_glyph_map[glyph] = std::string("tame ") + monster->mname;
    } else {
      fullscreen_view_glyph_map[glyph] = (mons[glyph_to_mon(glyph)].mname);
    }
  }
}

py::bytes NLELanguageObsv::text_cursor(py::array_t<int16_t> glyphs,
                                       py::array_t<int64_t> blstats,
                                       py::array_t<int64_t> tty_cursor) {
  py::buffer_info glyphs_buffer = glyphs.request();
  py::buffer_info blstats_buffer = blstats.request();
  py::buffer_info tty_cursor_buffer = tty_cursor.request();

  int16_t *glyphs_data = reinterpret_cast<int16_t *>(glyphs_buffer.ptr);
  int64_t *blstats_data = reinterpret_cast<int64_t *>(blstats_buffer.ptr);
  int64_t *tty_cursor_data = reinterpret_cast<int64_t *>(tty_cursor_buffer.ptr);

  int64_t player_x = blstats_data[0];
  int64_t player_y = blstats_data[1];
  int64_t cursor_x = tty_cursor_data[1];
  int64_t cursor_y = tty_cursor_data[0] - 1;  // Correct offset.

  int64_t glyph_relative_x = cursor_x - player_x;
  int64_t glyph_relative_y = -cursor_y + player_y;

  int64_t glyph_relative_start_0_x = glyph_relative_x + DUNGEON_WIDTH;
  int64_t glyph_relative_start_0_y = glyph_relative_y + DUNGEON_HEIGHT;

  std::string output;

  int64_t glyph_idx = cursor_x + cursor_y * DUNGEON_WIDTH;
  if ((glyph_relative_start_0_x >= 0) &&
      (glyph_relative_start_0_x < DUNGEON_WIDTH * 2) &&
      (glyph_relative_start_0_y >= 0) &&
      (glyph_relative_start_0_y < DUNGEON_HEIGHT * 2) && (glyph_idx > 0) &&
      (glyph_idx < glyphs.size())) {
    std::pair<std::string, std::string> distance_direction =
        screen_distance_direction_lookup[glyph_relative_start_0_x]
                                        [glyph_relative_start_0_y];

    int16_t glyph = glyphs_data[cursor_x + cursor_y * DUNGEON_WIDTH];

    std::string glyph_string = fullscreen_view_glyph_map[glyph];

    if (glyph_relative_x == 0 && glyph_relative_y == 0) {
      output = "Yourself a " + glyph_string;
    } else {
      output = distance_direction.first + " " + distance_direction.second +
               " " + glyph_string;
    }
  } else {
    output = "";
  }

  return py::bytes(output);
}

py::bytes NLELanguageObsv::text_glyphs(py::array_t<int16_t> glyphs,
                                       py::array_t<int64_t> blstats) {
  py::buffer_info glyphs_buffer = glyphs.request();
  py::buffer_info blstats_buffer = blstats.request();

  int16_t *glyphs_data = reinterpret_cast<int16_t *>(glyphs_buffer.ptr);
  int64_t *blstats_data = reinterpret_cast<int64_t *>(blstats_buffer.ptr);

  std::list<std::tuple<std::string, std::string, std::string>>
      glyph_distance_direction;

  glyph_distance_direction.splice(glyph_distance_direction.end(),
                                  fullscreen_view(glyphs_data, blstats_data));
  glyph_distance_direction.splice(glyph_distance_direction.end(),
                                  visual_view(glyphs_data, blstats_data));

  glyph_distance_direction =
      sort_by_distance_direction(glyph_distance_direction);

  glyph_distance_direction = compress_by_glyph(glyph_distance_direction);

  std::string output = "";
  uint64_t idx = 0;
  for (auto it = glyph_distance_direction.begin();
       it != glyph_distance_direction.end(); it++) {
    std::string glyphs_string = std::get<0>(*it);
    std::string distance_string = std::get<1>(*it);
    std::string directions_string = std::get<2>(*it);
    output += glyphs_string + " " + distance_string;
    output += " ";
    output += directions_string;
    if (idx + 1 < (glyph_distance_direction.size())) output += "\n";
    idx++;
  }
  return py::bytes(output);
}

py::bytes NLELanguageObsv::text_inventory(py::array_t<uint8_t> inv_strs,
                                          py::array_t<uint8_t> inv_letters) {
  py::buffer_info inv_strs_buffer = inv_strs.request();
  py::buffer_info inv_letters_buffer = inv_letters.request();
  uint8_t *inv_strs_data = reinterpret_cast<uint8_t *>(inv_strs_buffer.ptr);
  uint8_t *inv_letters_data =
      reinterpret_cast<uint8_t *>(inv_letters_buffer.ptr);
  size_t x = inv_strs_buffer.shape[0];
  size_t y = inv_strs_buffer.shape[1];

  std::string output = "";

  for (uint64_t i = 0; i < x; i++) {
    std::string inv_letter(1, inv_letters_data[i]);
    std::string inv_str(reinterpret_cast<char *>(&(inv_strs_data[i * y])));
    if (inv_letters_data[i] != 0) {
      if (i > 0) output += "\n";
      output += inv_letter + ": " + inv_str;
    } else
      break;
  }
  return py::bytes(output);
}

std::pair<std::string, std::string> NLELanguageObsv::pos_to_str(int x, int y) {
  int diag_dist = diagonal_distance(x, y);
  std::string diagonal = "";
  if (diag_dist > 0) {
    if (y < 0 && x < 0)
      diagonal = "southwest";
    else if (y < 0 && x > 0)
      diagonal = "southeast";
    else if (y > 0 && x < 0)
      diagonal = "northwest";
    else
      diagonal = "northeast";
  }
  int y_offset;
  int x_offset;
  if (y > 0)
    y_offset = y - diag_dist;
  else
    y_offset = y + diag_dist;
  if (x > 0)
    x_offset = x - diag_dist;
  else
    x_offset = x + diag_dist;

  std::string str_offset = offset_to_str(max(abs(x), abs(y)));

  std::string position_descriptor_x;
  std::string position_descriptor_y;

  if (x_offset < 0)
    position_descriptor_x = "west";
  else if (x_offset > 0)
    position_descriptor_x = "east";
  else
    position_descriptor_x = "";

  if (y_offset < 0)
    position_descriptor_y = "south";
  else if (y_offset > 0)
    position_descriptor_y = "north";
  else
    position_descriptor_y = "";

  std::string distance_str = str_offset;
  std::string direction_str =
      position_descriptor_y + position_descriptor_x + diagonal;
  return std::make_pair(distance_str, direction_str);
}

std::string NLELanguageObsv::offset_to_str(int offset) {
  if (offset == 1)
    return "adjacent";
  else if (offset == 2)
    return "very near";
  else if (offset > 2 && offset < 6)
    return "near";
  else if (offset > 5 && offset < 20)
    return "far";
  else
    return "very far";
}

int NLELanguageObsv::diagonal_distance(int dx, int dy) {
  dx = abs(dx);
  dy = abs(dy);
  int diagonal_steps = min(dx, dy);
  return diagonal_steps;
}

py::bytes NLELanguageObsv::text_blstats(py::array_t<int64_t> blstats) {
  py::buffer_info blstats_buffer = blstats.request();
  int64_t *blstats_data = reinterpret_cast<int64_t *>(blstats_buffer.ptr);

  std::string alignment_str;
  switch (blstats_data[26]) {
    case A_NONE:
      alignment_str = "None";
      break;
    case A_LAWFUL:
      alignment_str = "Lawful";
      break;
    case A_NEUTRAL:
      alignment_str = "Neutral";
      break;
    case A_CHAOTIC:
      alignment_str = "Chaotic";
      break;
  }

  std::string hunger_str;
  switch (blstats_data[21]) {
    case SATIATED:
      hunger_str = "Satiated";
      break;
    case NOT_HUNGRY:
      hunger_str = "Not Hungry";
      break;
    case HUNGRY:
      hunger_str = "Hungry";
      break;
    case WEAK:
      hunger_str = "Weak";
      break;
    case FAINTING:
      hunger_str = "Fainting";
      break;
    case FAINTED:
      hunger_str = "Fainted";
      break;
    case STARVED:
      hunger_str = "Starved";
      break;
  }

  std::string encumberance_str;
  switch (blstats_data[22]) {
    case UNENCUMBERED:
      encumberance_str = "Unemcumbered";
      break;
    case SLT_ENCUMBER:
      encumberance_str = "Burdened";
      break;
    case MOD_ENCUMBER:
      encumberance_str = "Stressed";
      break;
    case HVY_ENCUMBER:
      encumberance_str = "Strained";
      break;
    case EXT_ENCUMBER:
      encumberance_str = "Oveexrtaxed";
      break;
    case OVERLOADED:
      encumberance_str = "Overloaded";
      break;
  }

  std::string condition;
  std::vector<std::string> conditions;
  if (blstats_data[25] & BL_MASK_STONE) conditions.push_back("Stoned");
  if (blstats_data[25] & BL_MASK_SLIME) conditions.push_back("Slimed");
  if (blstats_data[25] & BL_MASK_STRNGL) conditions.push_back("Strangled");
  if (blstats_data[25] & BL_MASK_FOODPOIS)
    conditions.push_back("Food Poisoning");
  if (blstats_data[25] & BL_MASK_TERMILL)
    conditions.push_back("Terminally Ill");
  if (blstats_data[25] & BL_MASK_BLIND) conditions.push_back("Blind");
  if (blstats_data[25] & BL_MASK_DEAF) conditions.push_back("Deaf");
  if (blstats_data[25] & BL_MASK_STUN) conditions.push_back("Stunned");
  if (blstats_data[25] & BL_MASK_CONF) conditions.push_back("Confused");
  if (blstats_data[25] & BL_MASK_HALLU) conditions.push_back("Hallucinating");
  if (blstats_data[25] & BL_MASK_LEV) conditions.push_back("Levitating");
  if (blstats_data[25] & BL_MASK_FLY) conditions.push_back("Flying");
  if (blstats_data[25] & BL_MASK_RIDE) conditions.push_back("Riding");
  if (conditions.size() == 0)
    condition = "None";
  else if (conditions.size() == 1)
    condition = conditions[0];
  else if (conditions.size() > 1) {
    condition = conditions[0];
    for (auto it = ++conditions.begin(); it != conditions.end(); ++it) {
      condition += " " + *it;
    }
  }

  std::string output =
      ("Strength: " + std::to_string(blstats_data[3]) + "/" +
       std::to_string(blstats_data[2]) + "\n" +
       "Dexterity: " + std::to_string(blstats_data[4]) + "\n" +
       "Constitution: " + std::to_string(blstats_data[5]) + "\n" +
       "Intelligence: " + std::to_string(blstats_data[6]) + "\n" +
       "Wisdom: " + std::to_string(blstats_data[7]) + "\n" +
       "Charisma: " + std::to_string(blstats_data[8]) + "\n" +
       "Depth: " + std::to_string(blstats_data[12]) + "\n" +
       "Gold: " + std::to_string(blstats_data[13]) + "\n" +
       "HP: " + std::to_string(blstats_data[10]) + "/" +
       std::to_string(blstats_data[11]) + "\n" +
       "Energy: " + std::to_string(blstats_data[14]) + "/" +
       std::to_string(blstats_data[15]) + "\n" +
       "AC: " + std::to_string(blstats_data[16]) + "\n" +
       "XP: " + std::to_string(blstats_data[18]) + "/" +
       std::to_string(blstats_data[19]) + "\n" +
       "Time: " + std::to_string(blstats_data[20]) + "\n" +
       "Position: " + std::to_string(blstats_data[0]) + "|" +
       std::to_string(blstats_data[1]) + "\n" + "Hunger: " + hunger_str + "\n" +
       "Monster Level: " + std::to_string(blstats_data[17]) + "\n" +
       "Encumbrance: " + encumberance_str + "\n" +
       "Dungeon Number: " + std::to_string(blstats_data[23]) + "\n" +
       "Level Number: " + std::to_string(blstats_data[24]) + "\n" +
       "Score: " + std::to_string(blstats_data[9]) + "\n" +
       "Alignment: " + alignment_str + "\n" + "Condition: " + condition);
  return py::bytes(output);
}

std::string NLELanguageObsv::trim(std::string input) {
  const std::string WHITESPACE = " \32\0\n\r\t\f\v";
  size_t start = input.find_first_not_of(WHITESPACE);
  if (start == (input.size() - 1)) return "";
  std::string output = input.erase(0, start);
  size_t end = output.find_last_not_of(WHITESPACE, output.size() - 1);
  output = output.erase(end + 1, std::string::npos);
  return output;
}

py::bytes NLELanguageObsv::text_message(py::array_t<uint8_t> tty_chars) {
  py::buffer_info tty_chars_buffer = tty_chars.request();
  uint8_t *tty_chars_data = reinterpret_cast<uint8_t *>(tty_chars_buffer.ptr);

  size_t rows = tty_chars_buffer.shape[0];
  size_t columns = tty_chars_buffer.shape[1];
  std::string output = "";
  std::string first_row_str = "";
  bool multipage_message = false;

  std::string row_str(reinterpret_cast<char *>(&(tty_chars_data[0])), columns);
  size_t indent = row_str.find_first_not_of(' ');
  for (uint64_t row_idx = 0; row_idx < rows; row_idx++) {
    std::string row_str(reinterpret_cast<char *>(
                            &(tty_chars_data[indent + (row_idx * columns)])),
                        columns - indent);
    row_str = trim(row_str);
    if (row_idx == 0) {
      first_row_str = row_str;
      if (first_row_str == "") return py::bytes("");
    }
    size_t of_pos = row_str.find(" of ");
    multipage_message =
        (((of_pos != std::string::npos) && (row_str[of_pos - 2] == '(') &&
          (row_str[of_pos + 5] == ')')) ||
         (row_str.find("--More--") != std::string::npos) ||
         (row_str.find("(end)") != std::string::npos));
    output += row_str;
    if (multipage_message) return py::bytes(output);
    output += "\n";
  }
  return py::bytes(first_row_str);
}

}  // namespace nle_language_obsv
PYBIND11_MODULE(nle_language_obsv, m) {
  py::class_<nle_language_obsv::NLELanguageObsv>(m, "NLELanguageObsv")
      .def(py::init<>())
      .def("text_glyphs", &nle_language_obsv::NLELanguageObsv::text_glyphs,
           "Convert glyphs to text description")
      .def("text_blstats", &nle_language_obsv::NLELanguageObsv::text_blstats,
           "Convert blstats to text description")
      .def("text_inventory",
           &nle_language_obsv::NLELanguageObsv::text_inventory,
           "Convert inventory to text description")
      .def("text_cursor", &nle_language_obsv::NLELanguageObsv::text_cursor,
           "Convert tty_cursor to text description")
      .def("text_message", &nle_language_obsv::NLELanguageObsv::text_message,
           "Convert tty_chars to text message including menus");
}
