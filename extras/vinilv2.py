from extras.midiav2 import Midia


class Vinil(Midia):

    def exibir_ficha_tecnica(self):
        print("===== Ficha Técnica: Vinil (v2) =====")
        print(f"Título: {self.titulo}")
        print(f"Artista: {self.artista}")
        print(f"Data de lançamento: {self.data_lancamento}")
        print(f"Estado de conservação: {self.estado_conservacao}")