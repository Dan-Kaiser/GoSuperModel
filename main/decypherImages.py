import pyautogui
import numpy as np
import cv2

# Load reference images of tiles
reference_images = {
    "👠": cv2.imread("./referenceImages/highHeels.png"),
    "👖": cv2.imread("./referenceImages/pants.png"),
    "👜": cv2.imread("./referenceImages/purse.png"),
    "👚": cv2.imread("./referenceImages/top.png"),
    # Add more reference images as needed
}

# Define the coordinates of the game board (adjust these as per your screen resolution)
board_x = 1318  # X-coordinate of the top-left corner of the board
board_y = 428  # Y-coordinate of the top-left corner of the board
board_width = 372  # Width of the game board
board_height = 407  # Height of the game board
tile_width = 33
tile_height = 33

# Capture a screenshot of the game board
screenshot = pyautogui.screenshot(
    region=(board_x, board_y, board_width, board_height))

# Save the screenshot to a file
screenshot.save("./referenceImages/gameboard_screenshot.png")

# Create a 2D list to store individual tiles
tiles = []

# Initialize an empty game board to store matched tiles
game_board = np.empty((12, 11), dtype=object)

# Iterate through the game board and capture each tile
for row in range(12):
    tile_row = []
    for col in range(11):
        # Calculate the coordinates for the current tile
        left = col * tile_width + col
        upper = row * tile_height + row
        right = left + tile_width - 1
        lower = upper + tile_height - 1

        # Crop the tile from the screenshot
        tile = screenshot.crop((left, upper, right, lower))
        # Convert the tile image to a NumPy array
        tile_np = np.array(tile)
        # Append the tile image to the row
        tile_row.append(tile)

        best_match = None
        best_match_score = float('inf')  # Initialize with a high value

        for tile_name, reference_image in reference_images.items():
            # Resize the tile to match the size of the reference image
            tile_resized = cv2.resize(
                tile_np, (reference_image.shape[1], reference_image.shape[0]))

            # Calculate the absolute difference between the tile and reference image
            diff = cv2.absdiff(tile_resized, reference_image)
            # Sum of absolute differences as a matching score
            match_score = np.sum(diff)

            # Update best match if the current score is lower
            if match_score < best_match_score:
                best_match = tile_name
                best_match_score = match_score

        # Store the best match in the game board
        game_board[row, col] = best_match

    # Append the row of tiles to the tiles list
    tiles.append(tile_row)

# Save each tile as an image
for row in range(12):
    for col in range(11):
        tile = tiles[row][col]
        tile.save(f"./tileImages/tile_{row}_{col}.png")
        print(f"Tile ({row}, {col}): {game_board[row, col]}")

for row in range(12):
    print(f"{game_board[row]}")


print("Contents of each tile matched.")
