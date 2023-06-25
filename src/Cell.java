import java.awt.BorderLayout;
import java.awt.Color;

import javax.swing.JLabel;
import javax.swing.JPanel;

public class Cell {
    public static Integer x;
    public static Integer y;

    public static Integer value;
    public JPanel panel = new JPanel();

    private static BorderLayout bLayout = new BorderLayout();

    public Cell( Integer _x, Integer _y, Integer _value ){
        x = _x;
        y = _y;

        value = _value;

        panel.setLayout(bLayout);

        draw();
    }

    private void draw(){
        if( value >= 256 )
            panel.setBackground(Settings.COLOR_256_MORE);
        else{
            try {
                panel.setBackground( (Color) Settings.class.getField("COLOR_" + value.toString()).get(null) );
            } catch (IllegalArgumentException | IllegalAccessException | NoSuchFieldException | SecurityException e) {
                e.printStackTrace();
            }
        }

        JLabel label = new JLabel(value.toString());
        panel.add(label, BorderLayout.CENTER);
    }
}
