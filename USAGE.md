# 📖 Usage Guide

Follow these steps to set up and use the Angler Quest macro effectively.

## 🚀 Initial Setup

1.  **Launch the Application**: Run `python3 -m angler`.
2.  **Select Your Location**: On the **Home** tab, use the **Angler Location** dropdown to select your current in-game area (e.g., Moosewood, Sunstone). This loads the correct fish list for matching.
3.  **Prepare the Game**: Ensure Roblox is in windowed or borderless mode and the Fish bag/inventory is accessible.
4. **Untrack any other quests**: Make sure no other quests are tracked in the game.

---

## 🎯 Configuration

### 1. Capture Box Setup (Fish Recognition)
The capture box tells the macro where to look for the fish name provided by the Angler NPC.

1.  **Show the Box**: Press **F3** to toggle the blue capture box.
2.  **Position It**: Drag and resize the box so it covers the area where the fish name text appears.
3.  **Save & Hide**: Press **F3** again to save the position and hide the box.
    *   *Note: Ensure the background behind the text is not too bright for better OCR accuracy.*

![box_dialog](https://github.com/Moon-Playground/fisch-angler/raw/main/.github/assets/box_and_dialog.png)
*(Blue box = OCR Area | Green box = Dialogue Button)*

### 2. Click Coordinates Point
The macro needs to know where to click. Switch to the **Coordinates** tab and follow these steps for each point:

*   **Dialogue Interaction**:
    1. Click **Select** on the "Dialogue" section.
    2. Click **OK** on the popup.
    3. Hover your mouse over the "Yeah, there it is!" button in the NPC's dialogue.
    4. Press **R** to lock the coordinates.

*   **Search Bar Setup**:
    1. Open your **Inventory/Bag** in-game.
    2. Click **Select** on the "Search Bar" section in the macro.
    3. Hover your mouse over the search input field in your bag.
    4. Press **R** to lock.

*   **Fish Area (Inventory Slot)**:
    1. Click **Select** on the "Fish area" section.
    2. Hover your mouse over the **first slot** of your inventory (where the filtered fish will appear).
    3. Press **R** to lock.

![fish_search](https://github.com/Moon-Playground/fisch-angler/raw/main/.github/assets/fish_and_search.png)
*(Blue box = Fish Slot | Green box = Search Bar | Yellow = Favorites Toggle)*

---

## 🎣 Starting the Macro

1.  **Turn off Favorites**: It is highly recommended to disable the "Favorites" filter in your bag to prevent the macro from accidentally selecting the favorited fish.
2.  **Toggle Action**: Press **F4** to start the automation.
    *   The status overlay will change to **Active**.
    *   The macro will now interact with the NPC, read the required fish, search your bag, and turn it in.
3.  **To Stop**: Press **F4** again.

---

## 🛠️ Troubleshooting

-   **OCR failing?** Try resizing the capture box or moving to a spot with a darker background.
-   **Clicking wrong spots?** Re-set the coordinates in the **Coordinates** tab.
-   **Wrong fish selected?** Ensure "Favorites" is off and the search bar coordinates are precise.
-   **Exiting**: Press **F5** to close the application completely.
