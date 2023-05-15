import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
 
public class App extends Application {
    @Override
    public void start(Stage Stage) throws Exception {

  
        Parent root ;
        root = FXMLLoader.load(getClass().getResource("MainScene.fxml"));
        Scene scene = new Scene(root);
        Stage.setTitle("Audio Converter");
        Stage.setScene(scene);
        Stage.show();
    }
 public static void main(String[] args) {
        launch(args);
    }
}