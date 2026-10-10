# Lab 4 — Vibe Coding: Treasure Hunt Enhancements

## 1. Project Overview

This project enhances the existing **Treasure Hunt** game developed using Python and Pygame. The game features a procedurally generated dungeon in which the player must collect a key and reach the treasure chest.

The objective of this lab was to use an LLM as a coding assistant to understand, modify, debug, and test the existing game while keeping the implementation modular and understandable.

## 2. Implemented Features

### Task 1 — Floor Traps
- Added traps to suitable floor locations in the dungeon.
- When the player touches a trap, they return to the starting position.
- A status message informs the player that a trap has been triggered.

### Task 2 — Patrolling Enemy Guard
- Added an enemy guard near the treasure chest.
- The guard patrols back and forth between two points.
- Collision with the guard resets the player to the starting position and displays a status message.

### Task 3 — Real-Time Mini-Map
- Added a mini-map in the corner of the game screen.
- Walls and floor tiles are represented using different colours.
- The player's current position is marked and updated during gameplay.

### Task 4 — Inventory User Interface
- Added an inventory slot to the game's HUD.
- The slot is empty when the game starts.
- After the player collects the key, the inventory displays a key indicator.

## 3. Technologies Used

- **Programming language:** Python
- **Game library:** Pygame Community Edition (pygame-ce)
- **Development environment:** Visual Studio Code
- **Version control:** Git and GitHub
- **LLM assistance:** ChatGPT

## 4. Repository Structure

```text
Lab-4/
├── 24_treasure_hunt/
│   └── game.py
├── before_edit.mp4
├── after_trap.mp4
├── FINAL.mp4
└── README.md
```

The video filenames above should match the files actually uploaded to this repository. Remove or rename any entries that do not match the final submission.

## 5. Running the Game

Install the required library:

```bash
pip install pygame-ce
```

Navigate to the directory containing `game.py` and run:

```bash
python game.py
```

### Controls

| Key | Action |
|---|---|
| W / A / S / D | Move the player |
| Arrow keys | Move the player |
| R | Restart the game |

## 6. Testing and Verification

The following behaviours should be verified during gameplay:

- The player returns to the starting position after touching a trap.
- The guard patrols and resets the player when a collision occurs.
- The mini-map represents the dungeon layout and player position.
- The inventory slot updates when the key is collected.
- The player can collect the key and then reach the treasure chest.
- Restarting the game resets the game state correctly.

## 7. Gameplay Demonstrations

- **Before modifications:** `before_edit.mp4`
- **After modifications:** `FINAL.mp4`

The after-modification video should demonstrate the implemented features. Update the filenames in this section if your final video uses a different name.

## 8. LLM Chat History

The complete ChatGPT conversation documenting the assistance used during implementation, debugging, and testing is available here:

**[View Complete Chat History (PDF)](./Treasure_Hunt_Enhancements.pdf)**

The original conversation link is provided to support transparency and meet the lab's LLM chat-history requirement.

## 9. Summary

This lab demonstrates the use of LLM-assisted development to extend an existing Python game through incremental feature implementation, debugging, testing, and version control. The four enhancements improve gameplay through traps, an enemy guard, a mini-map, and an inventory interface.
