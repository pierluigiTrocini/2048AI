import java.awt.GridLayout;
import javax.swing.JFrame;

public class App {
    public static Cell[][] grid = new Cell[Settings.GRID_SIZE][Settings.GRID_SIZE];

    public static JFrame frame = new JFrame(Settings.title);
    public static GridLayout gridLayout = new GridLayout(
        Settings.GRID_SIZE, 
        Settings.GRID_SIZE, 
        Settings.GAP, 
        Settings.GAP
    );

    private static void initializeGrid(){
        for(int i = 0; i < Settings.GRID_SIZE; i++)
            for(int j = 0; j < Settings.GRID_SIZE; j++){
                grid[i][j] = new Cell(i, j, Utility.getInstance().randomValue());
                frame.add(grid[i][j].panel);
            }
    }

    public static void main(String[] args) throws Exception {
        frame.setSize(Settings.WINDOW_SIZE, Settings.WINDOW_SIZE);
        frame.setVisible(true);
        frame.setResizable(false);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        frame.setLayout(gridLayout);
        initializeGrid();
    }
}
