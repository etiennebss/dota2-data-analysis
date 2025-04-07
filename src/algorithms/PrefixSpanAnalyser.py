from prefixspan import PrefixSpan

class PrefixSpanAnalyser:
    def __init__(self, percent, sequences):
        """
        Constructeur de la classe `PrefixSpanAnalyser`.
        Cette méthode initialise l'instance en acceptant une valeur de pourcentage (`percent`)
        qui détermine le support minimal pour les motifs fréquents, et une liste de séquences
        (`sequences`) sur lesquelles l'algorithme de PrefixSpan sera appliqué.

        @param percent: Le pourcentage de support minimal pour détecter un motif fréquent.
                        Ce pourcentage sera converti en nombre de séquences à partir du total de séquences.
        @type percent: int
        @param sequences: Une liste de séquences d'éléments à analyser.
                          Chaque séquence est une liste d'éléments.
        @type sequences: list[list]
        """
        self.sequences = sequences

        if self.sequences:
            self.support = int(percent/100 * len(self.sequences))
        else:
            self.support = 0

        self.ps = PrefixSpan(self.sequences)
        self.frequents = self.detectionFrequentPattern()

    def detectionFrequentPattern(self):
        """
        Détecte les motifs fréquents dans les séquences selon le support défini.
        Cette méthode utilise l'algorithme PrefixSpan pour détecter les motifs fréquents dans les
        séquences données, en respectant le support minimal (défini dans le constructeur).

        @return: Une liste de motifs fréquents détectés, chaque élément de la liste étant un tuple
                 contenant le support (fréquence d'apparition) et le motif lui-même.
        @rtype: list of tuples
        """
        if self.support == 0:
            return []  # Retourne une liste vide si aucune séquence
        return self.ps.frequent(self.support, closed=True)

    def _majority(self, liste):
        elemUnique = []
        for elt in liste:
            if elt not in elemUnique:
                elemUnique.append(elt)
        return len(elemUnique)>len(liste)/2

    def export(self):
        copy = []
        for count, motif in self.frequents :
            if len(motif)>5 and self._majority(motif):
                copy.append((count, motif))
        return sorted(copy, key=lambda x: x[0], reverse=True)

    def printFrequentPattern(self):
        """
        Affiche les motifs fréquents détectés et leur nombre d'occurrences.
        Cette méthode affiche le nombre de motifs fréquents détectés, ainsi que chacun d'entre eux
        accompagné de son support (nombre d'occurrences). Les motifs sont triés par ordre décroissant
        de leur fréquence.

        @return: Aucun. La méthode imprime les motifs et leurs supports à l'écran.
        @rtype: None
        """
        print(f"Avec un support minimal de {self.support}, nous avons analysé {len(self.sequences)} séquences.\n")

        if not self.frequents:
            print("Aucun motif fréquent détecté.")
            return

        print(f"Nous avons détecté au total {len(self.frequents)} motifs, les voici :")

        sortedPatterns = sorted(self.frequents, key=lambda x: x[0], reverse=True)

        for support, motif in sortedPatterns:
            if (0.0,0.0) not in motif and len(motif)>= 4:
                print(f"Le motif {motif} a été détecté {support} fois.")

    def getLenMotif(self):
        return len(self.frequent)
