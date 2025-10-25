import cv2
from tkinter import Tk, filedialog
import numpy as np
from skimage.morphology import skeletonize
from skimage.filters import threshold_otsu
from typing import List, Optional, Tuple
import matplotlib.pyplot as plt

class BiometricSys:
    """
    Classe responsável pelas operações principais do sistema biométrico, incluindo
    extração de minúcias, geração de templates e comparação de impressões digitais.

    Attributes:
        tolerance (float): Tolerância máxima de distância para considerar dois pontos
            de minúcia como correspondentes durante a comparação.
    """

    def __init__(self, tolerance: float = 0.05):
        """
        Inicializa o sistema biométrico com o valor de tolerância especificado.

        Args:
            tolerance (float, opcional): Distância máxima entre minúcias para
                considerar uma correspondência válida. O padrão é 0.05.
        """
         
        self.tolerance = tolerance

    def extract_minutiae(self, image_path: str) -> List[Tuple[int, int, int]]:
        """
        Extrai as minúcias de uma imagem de impressão digital.

        O processo envolve:
            1. Carregar a imagem em escala de cinza.
            2. Aplicar suavização e binarização (método de Otsu).
            3. Realizar skeletonização.
            4. Identificar pontos de terminação e bifurcação.

        Args:
            image_path (str): Caminho para o arquivo da imagem (.bmp, .png, etc.).

        Returns:
            List[Tuple[int, int, int]]: Lista de tuplas representando as minúcias
            detectadas no formato (x, y, tipo), onde:
                - tipo = 1 → terminação (ridge ending)
                - tipo = 3 → bifurcação (bifurcation)

        Raises:
            ValueError: Se a imagem não puder ser carregada.
        """
        # 1 - Carregar imagem em grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Não foi possível carregar a imagem: {image_path}")

        # 2 - Binarização
        blurred = cv2.GaussianBlur(img, (5,5), 0)
        thresh_val = threshold_otsu(blurred)
        binary = blurred > thresh_val

        # 3 - Skeletonização
        skeleton = skeletonize(binary)

        # 4 - Extrair minutiae (ridge endings e bifurcações)
        minutiae = []
        for y in range(1, skeleton.shape[0]-1):
            for x in range(1, skeleton.shape[1]-1):
                if skeleton[y, x]:
                    neighborhood = skeleton[y-1:y+2, x-1:x+2]
                    count = np.sum(neighborhood) - 1
                    if count == 1 or count == 3:  # ridge ending ou bifurcação
                        minutiae.append((x, y, int(count)))
        return minutiae

    def generate_template(self, minutiae_points: List[Tuple[int, int, int]]) -> np.ndarray:
        """
        Converte as minúcias extraídas em um template biométrico normalizado.

        Args:
            minutiae_points (List[Tuple[int, int, int]]): Lista de pontos de minúcia.

        Returns:
            np.ndarray: Template biométrico no formato NumPy (N x 3),
            onde as coordenadas (x, y) são normalizadas entre 0 e 1.
        """
        if not minutiae_points:
            return np.array([])
        template = np.array(minutiae_points, dtype=np.float32)
        # Opcional: normalizar posições
        template[:,0] /= template[:,0].max()
        template[:,1] /= template[:,1].max()
        return template

    def compare_templates(self,template1: np.ndarray,template2: np.ndarray,tolerance: Optional[float] = None) -> float:
        """
        Compara dois templates biométricos e calcula o grau de similaridade entre eles.

        Args:
            template1 (np.ndarray): Template da primeira impressão digital.
            template2 (np.ndarray): Template da segunda impressão digital.
            tolerance (float, opcional): Tolerância máxima para correspondência de
                pontos. Se não for informada, usa o valor padrão da instância.

        Returns:
            float: Porcentagem de similaridade (0.0 a 100.0).

        Observação:
            - A correspondência é considerada válida quando o tipo de minúcia é igual
              e a distância entre pontos é menor ou igual à tolerância.
        """
        tol = tolerance if tolerance is not None else self.tolerance
        if template1.size == 0 or template2.size == 0:
            return 0.0

        matched = 0
        for x1, y1, type1 in template1:
            for x2, y2, type2 in template2:
                dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                if type1 == type2 and dist <= tolerance:
                    matched += 1
                    break  # evita múltiplos matches para o mesmo ponto

        
        return matched / max(len(template1), len(template2)) * 100

    def visualize_minutiae(self, image_path: str, minutiae_points: List[Tuple[int, int, int]], save_path: str = "output_minutiae.png", show: bool = True) -> np.ndarray:
        """
        Gera uma imagem visualizando os pontos de minúcia detectados na impressão digital.

        Cada tipo de minúcia é destacado:
            - Azul: terminação de linha (ridge ending)
            - Vermelho: bifurcação (bifurcation)

        Args:
            image_path (str): Caminho da imagem original da impressão digital.
            minutiae_points (List[Tuple[int, int, int]]): Lista de minúcias detectadas
                no formato (x, y, tipo).
            save_path (str, opcional): Caminho onde a imagem resultante será salva.
                O padrão é 'output_minutiae.png'.
            show (bool, opcional): Define se a imagem deve ser exibida na tela.
                O padrão é True.

        Returns:
            np.ndarray: Imagem gerada com os pontos de minúcia sobrepostos.

        Raises:
            ValueError: Se a imagem original não puder ser carregada.
        """
        # Carregar imagem original
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Não foi possível carregar a imagem: {image_path}")

        # Converter para RGB (para desenhar colorido)
        img_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Desenhar cada ponto
        for (x, y, m_type) in minutiae_points:
            if m_type == 1:  # ridge ending → azul
                cv2.circle(img_color, (x, y), 3, (0, 0, 255), -1)
            elif m_type == 3:  # bifurcação → vermelho
                cv2.circle(img_color, (x, y), 3, (255, 0, 0), -1)

        # Salvar imagem final
        cv2.imwrite(save_path, cv2.cvtColor(img_color, cv2.COLOR_RGB2BGR))

        # Exibir resultado
        if show:
            plt.figure(figsize=(6, 6))
            plt.imshow(img_color)
            plt.title("Pontos de Minúcia Detectados")
            plt.axis("off")
            plt.show()

        return img_color

    def get_img_path(self) -> str:
        """
        Obtém o caminho do arquivo de imagem da impressão digital.

        Returns:
            str: Caminho para a imagem a ser processada.
        """
        Tk().withdraw()  # Hide main Tk window
        image_path = filedialog.askopenfilename(
        title="Escolha a impressão a ser analizada (.bmp)",
        filetypes=[("BMP images", "*.bmp")]
    )

        if not image_path:
            print("Nunhuma imagem selecionada.")
            exit()

        else:
            return image_path