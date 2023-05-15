import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.stage.Stage ;
import com.gluonhq.charm.glisten.control.TextField; 

public class MainSceneController {

    @FXML
    private TextField tfTitle;

    @FXML
    void btnokclicked(ActionEvent event) {
        Stage mainWindow = (Stage) tfTitle.getScene().getWindow();
        String title = tfTitle.getText();
        mainWindow.setTitle(title);
    }

}
