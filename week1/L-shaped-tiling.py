import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
from matplotlib import gridspec
import os

class EducationalLTiling:
    def __init__(self, size):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.tile_id = 1
        self.steps = []  # Store each step for animation
        self.explanations = []  # Store explanations for each step
        
        # Pre-calculate maximum number of tiles needed
        self.max_tiles = (size * size - 1) // 3
        self.colors = self.generate_color_palette()
        
    def generate_color_palette(self):
        """Generate a consistent color palette for all tiles"""
        # Use a colormap that can handle up to max_tiles
        base_cmap = plt.cm.get_cmap('tab20')
        colors = ['white']  # Color 0: empty cells
        
        # Generate distinct colors for all possible tiles
        for i in range(self.max_tiles):
            color = base_cmap(i % 20)  # tab20 has 20 distinct colors
            # Make colors slightly lighter for better visibility
            if i >= 20:
                color = tuple(0.7 + 0.3 * c for c in color[:3]) + (color[3],)
            colors.append(color)
        
        return colors
    
    def set_missing_cell(self, row, col):
        """Mark a cell as missing"""
        self.missing_row, self.missing_col = row, col
        self.board[row, col] = -1
        
    def tile_board(self, top_row, left_col, size, missing_row, missing_col, depth=0):
        """Recursively tile the board and record steps"""
        if size == 1:
            return
        
        half = size // 2
        
        # Record the current state before placing tile
        self.record_step(f"Step {len(self.steps)+1}: Divide {size}×{size} board into {half}×{half} quadrants", 
                        depth, top_row, left_col, size, "divide")
        
        # Determine which quadrant contains the missing cell
        quadrant_names = ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"]
        quadrant = 0
        if missing_row < top_row + half:
            if missing_col >= left_col + half:
                quadrant = 1
        else:
            if missing_col < left_col + half:
                quadrant = 2
            else:
                quadrant = 3
        
        explanation = f"Missing cell is in {quadrant_names[quadrant]} quadrant"
        self.record_step(explanation, depth, top_row, left_col, size, "identify")
        
        # Place an L-shaped tile in the center
        placed_cells = []
        if quadrant != 0:
            self.board[top_row + half - 1, left_col + half - 1] = self.tile_id
            placed_cells.append((top_row + half - 1, left_col + half - 1))
        if quadrant != 1:
            self.board[top_row + half - 1, left_col + half] = self.tile_id
            placed_cells.append((top_row + half - 1, left_col + half))
        if quadrant != 2:
            self.board[top_row + half, left_col + half - 1] = self.tile_id
            placed_cells.append((top_row + half, left_col + half - 1))
        if quadrant != 3:
            self.board[top_row + half, left_col + half] = self.tile_id
            placed_cells.append((top_row + half, left_col + half))
        
        tile_explanation = f"Place L-tile #{self.tile_id} covering 3 cells around center"
        self.record_step(tile_explanation, depth, top_row, left_col, size, "place_tile", placed_cells)
        
        self.tile_id += 1
        
        # Recursively tile the four quadrants
        new_depth = depth + 1
        
        if quadrant == 0:
            self.tile_board(top_row, left_col, half, missing_row, missing_col, new_depth)
            self.tile_board(top_row, left_col + half, half, top_row + half - 1, left_col + half, new_depth)
            self.tile_board(top_row + half, left_col, half, top_row + half, left_col + half - 1, new_depth)
            self.tile_board(top_row + half, left_col + half, half, top_row + half, left_col + half, new_depth)
        elif quadrant == 1:
            self.tile_board(top_row, left_col, half, top_row + half - 1, left_col + half - 1, new_depth)
            self.tile_board(top_row, left_col + half, half, missing_row, missing_col, new_depth)
            self.tile_board(top_row + half, left_col, half, top_row + half, left_col + half - 1, new_depth)
            self.tile_board(top_row + half, left_col + half, half, top_row + half, left_col + half, new_depth)
        elif quadrant == 2:
            self.tile_board(top_row, left_col, half, top_row + half - 1, left_col + half - 1, new_depth)
            self.tile_board(top_row, left_col + half, half, top_row + half - 1, left_col + half, new_depth)
            self.tile_board(top_row + half, left_col, half, missing_row, missing_col, new_depth)
            self.tile_board(top_row + half, left_col + half, half, top_row + half, left_col + half, new_depth)
        else:
            self.tile_board(top_row, left_col, half, top_row + half - 1, left_col + half - 1, new_depth)
            self.tile_board(top_row, left_col + half, half, top_row + half - 1, left_col + half, new_depth)
            self.tile_board(top_row + half, left_col, half, top_row + half, left_col + half - 1, new_depth)
            self.tile_board(top_row + half, left_col + half, half, missing_row, missing_col, new_depth)
    
    def record_step(self, explanation, depth, top_row, left_col, size, step_type, placed_cells=None):
        """Record the current state for visualization"""
        step_data = {
            'board': self.board.copy(),
            'explanation': explanation,
            'depth': depth,
            'region': (top_row, left_col, size, size),
            'step_type': step_type,
            'placed_cells': placed_cells if placed_cells else []
        }
        self.steps.append(step_data)
        self.explanations.append(explanation)

    def visualize_step_by_step(self, save_gif=True, save_mp4=False):
        """Create an animated step-by-step visualization and save as GIF"""
        fig = plt.figure(figsize=(15, 8))
        gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
        
        ax_board = plt.subplot(gs[0])
        ax_explain = plt.subplot(gs[1])
        
        # Remove axes from explanation panel
        ax_explain.axis('off')
        
        # Create consistent colormap
        custom_cmap = ListedColormap(self.colors)
        
        def animate(frame):
            ax_board.clear()
            ax_explain.clear()
            ax_explain.axis('off')
            
            step = self.steps[frame]
            board_state = step['board']
            explanation = step['explanation']
            top_row, left_col, size, _ = step['region']
            
            # Plot the board with consistent colors
            # Map values: -1 (missing) -> 0, 0 (empty) -> 0, tile_id -> tile_id
            plot_data = np.where(board_state == -1, 0, board_state)
            im = ax_board.imshow(plot_data, cmap=custom_cmap, vmin=0, vmax=self.max_tiles)
            
            # Highlight current region being processed
            rect = patches.Rectangle(
                (left_col - 0.5, top_row - 0.5), 
                size, size, 
                linewidth=3, 
                edgecolor='blue', 
                facecolor='none',
                alpha=0.7
            )
            ax_board.add_patch(rect)
            
            # Highlight newly placed cells
            for cell in step['placed_cells']:
                rect_cell = patches.Rectangle(
                    (cell[1] - 0.5, cell[0] - 0.5), 
                    1, 1, 
                    linewidth=2, 
                    edgecolor='green', 
                    facecolor='none'
                )
                ax_board.add_patch(rect_cell)
            
            # Mark the original missing cell with red border
            missing_patch = patches.Rectangle(
                (self.missing_col - 0.5, self.missing_row - 0.5), 
                1, 1, 
                linewidth=3, 
                edgecolor='red', 
                facecolor='none'
            )
            ax_board.add_patch(missing_patch)
            
            # Add grid and labels
            for i in range(self.size + 1):
                ax_board.axhline(i - 0.5, color='black', linewidth=0.5)
                ax_board.axvline(i - 0.5, color='black', linewidth=0.5)
            
            # Add cell numbers
            for i in range(self.size):
                for j in range(self.size):
                    if board_state[i, j] > 0:  # Only label placed tiles
                        ax_board.text(j, i, str(board_state[i, j]), 
                                    ha='center', va='center', fontweight='bold', 
                                    fontsize=8, color='black' if self.colors[board_state[i, j]][:3] > (0.6, 0.6, 0.6) else 'white')
            
            ax_board.set_xticks(np.arange(self.size))
            ax_board.set_yticks(np.arange(self.size))
            ax_board.set_title(f'Step {frame+1}/{len(self.steps)} - {size}×{size} Region', fontsize=14)
            
            # Add explanation
            ax_explain.text(0.1, 0.9, explanation, transform=ax_explain.transAxes, 
                          fontsize=12, verticalalignment='top', wrap=True)
            
            # Add recursion depth indicator
            depth_info = f"Recursion Depth: {step['depth']}"
            ax_explain.text(0.1, 0.7, depth_info, transform=ax_explain.transAxes, 
                          fontsize=11, style='italic')
            
            # Add algorithm explanation
            algo_text = "Algorithm Steps:\n1. Divide board into 4 quadrants\n2. Identify quadrant with missing cell\n3. Place L-tile in center\n4. Recursively solve each quadrant"
            ax_explain.text(0.1, 0.5, algo_text, transform=ax_explain.transAxes, 
                          fontsize=10, verticalalignment='top')
            
            # Add color legend for current tiles
            current_tiles = np.unique(board_state[board_state > 0])
            if len(current_tiles) > 0:
                # Show tile numbers horizontally in a single line
                legend_text = "Current Tiles: " + ", ".join(str(tile_id) for tile_id in current_tiles)
                ax_explain.text(0.1, 0.3, legend_text, transform=ax_explain.transAxes, 
                                fontsize=10, verticalalignment='top')
            
            plt.tight_layout()
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=len(self.steps), interval=2000, repeat=False)
        
        # Save as GIF
        if save_gif:
            print("Saving animation as GIF...")
            gif_path = f"l_tiling_animation_{self.size}x{self.size}_missing_{self.missing_row}_{self.missing_col}.gif"
            anim.save(gif_path, writer='pillow', fps=1, dpi=100)
            print(f"Animation saved as: {gif_path}")
       
        # Save as MP4
        if save_mp4:
            print("Saving animation as MP4...")
            mp4_path = f"l_tiling_animation_{self.size}x{self.size}_missing_{self.missing_row}_{self.missing_col}.mp4"
            anim.save(mp4_path, writer='ffmpeg', fps=1, dpi=100)
            print(f"Animation saved as: {mp4_path}")
            plt.tight_layout()
            plt.show()
            
        return anim
    
    def create_final_visualization(self, save_png=True):
        """Create a final comprehensive visualization and save as PNG"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Create consistent colormap
        custom_cmap = ListedColormap(self.colors)
        
        # Prepare data for plotting (map -1 to 0 for consistent coloring)
        plot_data = np.where(self.board == -1, 0, self.board)
        
        # Final board visualization
        im = ax1.imshow(plot_data, cmap=custom_cmap, vmin=0, vmax=self.max_tiles)
        
        # Add grid and missing cell
        for i in range(self.size + 1):
            ax1.axhline(i - 0.5, color='black', linewidth=1)
            ax1.axvline(i - 0.5, color='black', linewidth=1)
        
        # Mark missing cell with red border
        missing_patch = patches.Rectangle(
            (self.missing_col - 0.5, self.missing_row - 0.5), 
            1, 1, 
            linewidth=3, 
            edgecolor='red', 
            facecolor='none',
            label='Missing Cell'
        )
        ax1.add_patch(missing_patch)
        
        # Add tile numbers with contrasting text color
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] > 0:
                    # Choose text color based on background brightness
                    bg_color = self.colors[self.board[i, j]]
                    text_color = 'black' if sum(bg_color[:3]) / 3 > 0.6 else 'white'
                    ax1.text(j, i, str(self.board[i, j]), 
                            ha='center', va='center', fontweight='bold',
                            color=text_color, fontsize=10)
        
        ax1.set_title(f'Final Tiling - {self.size}×{self.size} Board\nMissing Cell at ({self.missing_row},{self.missing_col})', 
                     fontsize=14)
        ax1.legend()
        
        # Algorithm explanation
        ax2.axis('off')
        explanation_text = [
            "L-Shaped Tiling Algorithm",
            "=" * 30,
            f"Board Size: {self.size}×{self.size} (2^{int(np.log2(self.size))})",
            f"Missing Cell: ({self.missing_row}, {self.missing_col})",
            f"Total Tiles Used: {self.tile_id - 1}",
            "",
            "Divide and Conquer Approach:",
            "1. DIVIDE: Split board into 4 equal quadrants",
            "2. IDENTIFY: Find which quadrant has missing cell",
            "3. PLACE: Put L-tile in center, covering 3 quadrants",
            "4. RECURSE: Solve each quadrant recursively",
            "5. BASE CASE: Stop when quadrant size is 1",
            "",
            "Key Insight:",
            "• Each recursive call creates a new 'missing' cell",
            "• L-tiles always cover 3 of the 4 center cells",
            "• Algorithm guarantees complete coverage",
            "",
            f"• Total steps: {len(self.steps)}",
            f"• Maximum possible tiles: {self.max_tiles}",
            f"• Actual tiles used: {self.tile_id - 1}"
        ]
        
        for i, line in enumerate(explanation_text):
            ax2.text(0.1, 0.95 - i*0.04, line, transform=ax2.transAxes, 
                    fontsize=10 if i > 4 else 12,
                    fontweight='bold' if i <= 4 else 'normal',
                    verticalalignment='top')
        
        plt.tight_layout()
        
        # Save as PNG
        if save_png:
            print("Saving final result as PNG...")
            png_path = f"l_tiling_final_{self.size}x{self.size}_missing_{self.missing_row}_{self.missing_col}.png"
            plt.savefig(png_path, dpi=300, bbox_inches='tight')
            print(f"Final result saved as: {png_path}")
        
        plt.show()
    
    def solve_educational(self, missing_row, missing_col):
        """Complete educational solution with file output"""
        print(f"Solving L-Tiling for {self.size}×{self.size} board with missing cell at ({missing_row},{missing_col})")
        print("=" * 60)
        
        # Create output directory if it doesn't exist
        os.makedirs('tiling_output', exist_ok=True)
        
        self.set_missing_cell(missing_row, missing_col)
        self.tile_board(0, 0, self.size, missing_row, missing_col)
        
        print(f"\nSolution Complete!")
        print(f"Total steps: {len(self.steps)}")
        print(f"Tiles used: {self.tile_id - 1}")
        print(f"Maximum possible tiles: {self.max_tiles}")
        
        # Show step-by-step animation and save GIF
        print("\nGenerating step-by-step animation...")
        self.visualize_step_by_step(save_gif=True, save_mp4=True)
        
        # Show final result and save PNG
        print("\nGenerating final result...")
        self.create_final_visualization(save_png=True)
        
        print("\n" + "=" * 60)
        print("Files saved in current directory:")
        print(f"- l_tiling_animation_{self.size}x{self.size}_missing_{self.missing_row}_{self.missing_col}.gif")
        print(f"- l_tiling_final_{self.size}x{self.size}_missing_{self.missing_row}_{self.missing_col}.png")
        print("=" * 60)

# Example with your specific case
if __name__ == "__main__":
    # Create a 8x8 board (2^3)
    board_size = 8
    educational_tiling = EducationalLTiling(board_size)
    
    # Set missing cell at (3,1) as requested
    missing_row, missing_col = 3, 1
    
    # Solve with educational visualization and save files
    educational_tiling.solve_educational(missing_row, missing_col)