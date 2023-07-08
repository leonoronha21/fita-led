#include <Adafruit_GFX.h>
#include <Adafruit_NeoPixel.h>
#include <Adafruit_NeoMatrix.h>
#include <avr/pgmspace.h>

// Configuração da Matriz de Led
// Pino onde a matriz está conectada ao arduino, se você soldou em um pino diferente do 6 mude o script aqui
int pinLed = 6;
// Quantidade de Leds por linha
int width = 18;
// Quantidade de linhas
int height = 8;

// ATENÇÃO: Se você fizer sua matriz em um tamanho diferente, não vai bastar mudar as variáveis acima, 
// você precisa refazer as matrizes dos desenhos abaixo

// Essa é a configuração da Matriz, ela indica a ordem que foi feito o zigzag, se você optou por montar a matriz de outra forma
// boa sorte adaptando essa parte do código, mas você encontra mais informações na documentação original
Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(width, height, pinLed,
  NEO_MATRIX_TOP + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB + NEO_KHZ800);

// Configuração da detecção de som, não precisa mexer aqui, a menos que você queira, aí é problema seu
bool silent = false;
long silenttimer = 0;
unsigned long last_face = 0;

// Esses são os desenhos da máscara, cada variável contém toda a matriz para cada frame do desenho
// Cada linha aqui é uma linha de Leds, false é uma linha apagada e true é uma linha acesa

// Boca completamente fechada
const bool mount_0[] PROGMEM = {
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,true,true,true,true,true,true,true,true,true,true,true,true,true,true,false,false,
  false,false,true,true,true,true,true,true,true,true,true,true,true,true,true,true,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false
};

// Boca levemente aberta
const bool mount_1[] PROGMEM = {
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,true,true,true,true,true,true,true,true,true,true,true,true,true,true,false,false,
  false,false,true,false,false,false,false,false,false,false,false,false,false,false,false,true,false,false,
  false,false,false,true,true,true,true,true,true,true,true,true,true,true,true,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false
};

// Boca um pouco mais aberta
const bool mount_2[] PROGMEM = {
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,true,true,true,true,true,true,true,true,true,true,false,false,false,false,
  false,false,true,true,false,false,false,false,false,false,false,false,false,false,true,true,false,false,
  false,false,true,false,false,false,false,false,false,false,false,false,false,false,false,true,false,false,
  false,false,false,true,false,false,false,false,false,false,false,false,false,false,true,false,false,false,
  false,false,false,false,true,true,true,true,true,true,true,true,true,true,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false
};

// Boca quase aberta
const bool mount_3[] PROGMEM = {
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,true,true,true,true,true,true,true,true,true,true,false,false,false,false,false,
  false,false,false,true,false,false,false,false,false,false,false,false,false,false,true,false,false,false,
  false,false,false,true,false,false,false,false,false,false,false,false,false,false,true,false,false,false,
  false,false,false,true,true,false,false,false,false,false,false,false,false,true,true,false,false,false,
  false,false,false,false,false,true,true,true,true,true,true,true,true,false,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false
};

// Boca aberta
const bool mount_4[] PROGMEM = {
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
  false,false,false,false,true,true,true,true,true,true,true,true,true,true,false,false,false,false,
  false,false,false,true,false,false,false,false,false,false,false,false,false,false,true,false,false,false,
  false,false,false,true,false,false,false,false,false,false,false,false,false,false,true,false,false,false,
  false,false,false,true,false,false,false,false,false,false,false,false,false,false,true,false,false,false,
  false,false,false,false,true,false,false,false,false,false,false,false,false,true,false,false,false,false,
  false,false,false,false,false,true,true,true,true,true,true,true,true,false,false,false,false,false,
  false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false
};

// Boca escancarada 
const bool mount_5[] PROGMEM = {
  false,false,false,false,false,false,true,true,true,true,true,true,false,false,false,false,false,false,
  false,false,false,false,true,true,false,false,false,false,false,false,true,true,false,false,false,false,
  false,false,false,true,false,false,false,false,false,false,false,false,false,false,true,false,false,false,
  false,false,false,true,false,false,false,false,false,false,false,false,false,false,true,false,false,false,
  false,false,false,true,false,false,false,false,false,false,false,false,false,false,true,false,false,false,
  false,false,false,true,false,false,false,false,false,false,false,false,false,false,true,false,false,false,
  false,false,false,false,true,false,false,false,false,false,false,false,false,true,false,false,false,false,
  false,false,false,false,false,true,true,true,true,true,true,true,true,false,false,false,false,false
};
// Essa função é responsável por desenhar algum dos desenhos na matriz
void drawImage(short image_addr){
  // Limpa a matriz
  matrix.clear();
  
  // Loop para ir em cada posição e desenhar pixel a pixel
  for(int x = 0; x<width; x++){
    for(int y = 0; y<height; y++){
      bool light = pgm_read_byte(image_addr+x+y*width);

      // Acende se for pra acender
      if (light) {
        // em matrix.Color você pode mudar a cor do led cada parâmetro é uma cor de RGB, os valores vão de 0 a 255, nesse exemplo ele acende em branco
        matrix.drawPixel(x, y, matrix.Color(000,0,200));  
      }
    }
  }

  // Recarrega a matrix com o novo desenho
  matrix.show();
}

void setup() {
  // O setup prepara tudo para rodar
  
  // Inicializa a matriz NeoPixel
  matrix.begin();
  
  // Configura o brilho, uma atenção o brilho vai de 0 a 255, eu achei 50 mais que o suficiente para aparecer bem,
  // mas se o tecido da sua mascara for muito grosso pode ser que precise aumentar, mas uma dica, não aumente muito
  // se a luz for muito forte o circuito pode não dar conta e ele desligar, além de que com um brilho maior os leds tendem
  // a esquentar demais, eu achei 50 confortável
  matrix.setBrightness(60);
  
  // Configuro o serial, assim da pra ver a medida de volume do microfone via terminal e ajusta-lo
  Serial.begin(9600);
}

float vol = 0;
const uint16_t samples = 128;

void loop() {
  // Toda essa parte abaixo é responsável por detectar variação de volume e guardar o valor em uma variável
  float nvol = 0;
  int previous_peak = -1;
  
  for (int i = 0; i<samples; i++){
      auto analog = analogRead(A0);
      auto micline = abs(analog - 512);

      nvol = max(micline, nvol);
  }

  vol = (nvol + 1.0*vol)/2.0;

  // Imprime o volume via serial, assim da pra checar se o microfone está muito sensível e ajustar
  Serial.println(vol);

  // Desenha as bocas baseado na intencidade do volume
  if(vol < 180){
      if (silent == false) {
        silenttimer = millis() + 5000;
        silent = true;
        drawImage(mount_0);
      } else {
        if (silenttimer < millis()) {
          matrix.clear();
          matrix.show();
        }
      }
  } else if(vol < 300){
      silent = false;
      drawImage(mount_1);
  } else if(vol < 360){
      silent = false;
      drawImage(mount_2);
  } else if(vol < 500){
      silent = false;
      drawImage(mount_3);
  } else if(vol < 560){
      silent = false;
      drawImage(mount_4);
  } else {   
      silent = false;
      drawImage(mount_5);
  }
}
