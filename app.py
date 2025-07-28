using UnityEngine;
using UnityEngine.UI;

public class PinocytoseDetector : MonoBehaviour
{
    public int absorcoes = 0;
    public Text contadorText;

    void OnTriggerEnter2D(Collider2D outro)
    {
        if (outro.gameObject.tag == "Particula")
        {
            Destroy(outro.gameObject);
            absorcoes++;
            contadorText.text = "Absorções: " + absorcoes;
        }
    }
}
