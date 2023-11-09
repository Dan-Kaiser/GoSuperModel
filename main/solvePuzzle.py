import pyautogui
import cv2
import numpy as np
import math

# Load reference images of tiles
reference_images = {
    "👠": cv2.imread("./referenceImages/highHeels.png"),
    "👖": cv2.imread("./referenceImages/pants.png"),
    "👜": cv2.imread("./referenceImages/purse.png"),
    "👚": cv2.imread("./referenceImages/top.png"),
    "⬜": cv2.imread("./referenceImages/empty.png"),
    # Add more reference images as needed
}

# Define the coordinates of the game board (adjust these as per your screen resolution)
board_x = 1318  # X-coordinate of the top-left corner of the board
board_y = 428  # Y-coordinate of the top-left corner of the board
board_width = 372  # Width of the game board
board_height = 407  # Height of the game board
tile_width = 33
tile_height = 33

cursor_starting_height = math.ceil(board_y + ((tile_height + 1) / 2))
cursor_starting_width = math.ceil(board_x + ((tile_width + 1) / 2))
tile_x = 0
tile_y = 0

# Capture a screenshot of the game board
screenshot = pyautogui.screenshot(
    region=(board_x, board_y, board_width, board_height))

# Save the screenshot to a file
screenshot.save("./referenceImages/gameboard_screenshot.png")

# Create a 2D list to store individual tiles
tiles = []

# List to store actions (row and column coordinates)
actions = []
final_actions = []

# Initialize an empty game board to store matched tiles
game_board = np.empty((12, 11), dtype=object)
original_game_board = np.empty((12, 11), dtype=object)

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

        best_match = "⬜"
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

original_game_board = np.copy(game_board)

# Print the starting state of the game board
print("starting state of the gameboard")
for row in range(12):
    print(f"{game_board[row]}")


##                           ##
##                           ##
# BOARD DONE BUILDING HERE   ##
##                           ##
##                           ##


# Function to find a group of matching tiles
def find_group(row, col, tile):
    stack = [(row, col)]
    matching_group = []

    while stack:
        row, col = stack.pop()

        # Check if the current tile is out of bounds, does not match the target tile,
        # or has already been marked for removal
        if (
            row < 0
            or row >= 12
            or col < 0
            or col >= 11
            or game_board[row, col] != tile
            or game_board[row, col] == "⬜"
            or game_board[row, col][0] == "X"
        ):
            continue

        # Mark the tile is temporarly removed, before checking length of group.
        game_board[row, col] = "X" + game_board[row, col]
        # Add the current tile to the matching group
        matching_group.append((row, col))
        # Add adjacent tiles to the stack
        stack.extend(
            [
                (row - 1, col),  # Check above
                (row + 1, col),  # Check below
                (row, col - 1),  # Check left
                (row, col + 1),  # Check right
            ]
        )
    if (len(matching_group) > 1):
        # Mark tiles for removal and return group to be removed
        for group_tile in matching_group:
            game_board[group_tile[0], group_tile[1]] = "marked for removal"
        return matching_group
    else:
        # Remove the X from the tile if the group is not big enough
        for group_tile in matching_group:
            game_board[group_tile[0], group_tile[1]
                       ] = game_board[group_tile[0], group_tile[1]].replace("X", "")
        return []

# Function to fill blanks below a column


def fill_blanks_below():
    for col in range(11):
        for row in range(11, 0, -1):
            if game_board[row, col] == "⬜":
                # Find the nearest non-empty tile above
                for k in range(row - 1, -1, -1):
                    if game_board[k, col] != "⬜":
                        game_board[row, col] = game_board[k, col]
                        game_board[k, col] = "⬜"
                        break

# Function to move columns to the right to fill blanks


def move_columns_to_right():
    for col in range(10, 0, -1):
        if all(game_board[:, col] == "⬜"):
            # Move the entire column to the right
            for j in range(col, 0, -1):
                for i in range(12):
                    game_board[i, j] = game_board[i, j - 1]
                    game_board[i, j - 1] = "⬜"


def is_board_empty(board):
    return np.all(board == "⬜")


# Continue removing matching groups until only "⬜"s are left

# Give the function a whole game board copy in it's recursion, and test at each point if the gameboard is all empty

def recursion(board, actions_list, row, col):
    print(row, col)
    # check if final condition is met
    if (is_board_empty(board)):
        # set final actions to action_list
        final_actions = py.copy(actions_list)
        return
    else:
        # do the action at the point
        tile = board[row, col]
        group_to_remove = find_group(row, col, tile)
        # remove the tiles
        if len(group_to_remove) > 1:
            for group_tile in group_to_remove:
                game_board[group_tile[0], group_tile[1]] = "⬜"

                # Fill blanks below columns and move columns to the right as needed
                fill_blanks_below()
                move_columns_to_right()

        # Fill blanks below columns and move columns to the right as needed
        fill_blanks_below()
        move_columns_to_right()

        # record the action
        actions_list.append((row, col))

        new_col = col
        new_row = row
        # increment the col/row
        if (col < 10):
            new_col = new_col + 1
        elif (col == 10 and row < 11):
            new_row = new_row + 1
            new_col = 0
        else:
            return []

        print("new row, col", new_row, new_col)
        # call the function again
        return recursion(np.copy(board), actions_list, new_row, new_col)
# final_actions = recursion(np.copy(game_board), [], 0, 0)


# # while not is_board_empty:
for row in range(12):
    for col in range(11):
        print(row, col)
        tile = game_board[row, col]
        if tile != "⬜" and tile != "marked for removal":
            # Find a matching group starting from this tile
            group_to_remove = find_group(row, col, tile)
            # If the group has more than one tile, remove it and record actions
            if len(group_to_remove) > 1:
                for group_tile in group_to_remove:
                    game_board[group_tile[0], group_tile[1]] = "⬜"
                # Record the action (row and column coordinates)
                actions.append((row, col))
                # Fill blanks below columns and move columns to the right as needed
                fill_blanks_below()
                move_columns_to_right()
        fill_blanks_below()
        move_columns_to_right()


# Print the final state of the game board
print("final state of the gameboard")
for row in range(12):
    print(f"{game_board[row]}")


# Print the list of actions (row and column coordinates)
print("Actions:")
for action in actions:
    print(f"Click on tile at: X {action[1] + 1}, Y {action[0] + 1}")
    tile_x = cursor_starting_width + (tile_width * action[1]) + action[1]
    tile_y = cursor_starting_height + (tile_height * action[0]) + action[0]
    # Uncomment the two lines below to have the program move the mouse for you
    # pyautogui.moveTo(tile_x, tile_y, duration=.5)
    # pyautogui.click()
    print(f"Click on tile at: X {tile_x}, Y {tile_y}")

print("Puzzle solved.")

# print(pyautogui.position())
