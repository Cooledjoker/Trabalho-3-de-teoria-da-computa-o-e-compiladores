import graphviz
class AFN:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.estado_inicial = ""
        self.estados_aceitacao = set()
        self.transicoes = {}  # {(estado, símbolo): {conjunto_de_estados}}

    def ler_quintupla(self):
        print("=== DEFINIÇÃO DO AFN ===\n")

        # Conjunto de estados
        while True:
            estados_input = input("Q (estados, separados por vírgula): ").strip()
            if estados_input:
                self.estados = {q.strip() for q in estados_input.split(',')}
                break
            print("Erro: conjunto de estados não pode ser vazio")

        # Alfabeto
        while True:
            alfabeto_input = input("Σ (alfabeto, símbolos separados por vírgula; use 'ε' para epsilon): ").strip()
            if alfabeto_input:
                self.alfabeto = {s.strip() for s in alfabeto_input.split(',')} - {''}
                break
            print("Erro: alfabeto não pode ser vazio")

        # Estado inicial
        while True:
            self.estado_inicial = input("q0 (estado inicial): ").strip()
            if self.estado_inicial in self.estados:
                break
            print(f"Erro: estado inicial deve estar em {self.estados}")

        # Estados de aceitação
        while True:
            aceitacao_input = input("F (estados de aceitação, separados por vírgula): ").strip()
            if aceitacao_input:
                estados_aceitacao = {q.strip() for q in aceitacao_input.split(',')}
                self.estados_aceitacao = estados_aceitacao.intersection(self.estados)
                if self.estados_aceitacao:
                    break
                print(f"Erro: pelo menos um estado deve estar em {self.estados}")
            else:
                print("Erro: conjunto de estados de aceitação não pode ser vazio")

        # Função de transição
        print("\nδ (função de transição):")
        print("Formato: estado,símbolo,novo_estado")
        print("Exemplo: q0,0,q1")
        print("Aceita várias transições para o mesmo símbolo.")
        print("Use 'ε' para transições epsilon.")
        print("Digite 'fim' para terminar.\n")

        self.transicoes = {}
        while True:
            entrada = input("Transição: ").strip()
            if entrada.lower() == 'fim':
                break

            try:
                partes = [p.strip() for p in entrada.split(',')]
                if len(partes) != 3:
                    print("Erro: formato deve ser estado,símbolo,novo_estado")
                    continue

                estado, simbolo, novo_estado = partes

                if estado not in self.estados:
                    print(f"Erro: estado {estado} não está em {self.estados}")
                    continue

                if novo_estado not in self.estados:
                    print(f"Erro: novo estado {novo_estado} não está em {self.estados}")
                    continue

                if simbolo != "ε" and simbolo not in self.alfabeto:
                    print(f"Erro: símbolo {simbolo} não está no alfabeto {self.alfabeto} ou não é ε")
                    continue

                chave = (estado, simbolo)
                if chave not in self.transicoes:
                    self.transicoes[chave] = set()

                self.transicoes[chave].add(novo_estado)
                print(f"Transição adicionada: δ({estado}, {simbolo}) → {self.transicoes[chave]}")

            except Exception as e:
                print(f"Erro ao processar transição: {e}")

    def epsilon_fecho(self, estados):
        """Retorna o fecho-ε de um conjunto de estados."""
        pilha = list(estados)
        fechado = set(estados)

        while pilha:
            estado = pilha.pop()
            chave = (estado, "ε")
            if chave in self.transicoes:
                for destino in self.transicoes[chave]:
                    if destino not in fechado:
                        fechado.add(destino)
                        pilha.append(destino)

        return fechado

    def processar_cadeia(self, cadeia):
        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                print(f"Erro: símbolo '{simbolo}' não pertence ao alfabeto {self.alfabeto}")
                return False

        print(f"\nProcessando cadeia: {cadeia}")

        # Começa pelo ε-fecho do inicial
        atuais = self.epsilon_fecho({self.estado_inicial})
        print(f"Estados iniciais após ε-fecho: {atuais}")

        for simbolo in cadeia:
            proximos = set()

            for estado in atuais:
                chave = (estado, simbolo)
                if chave in self.transicoes:
                    proximos |= self.transicoes[chave]

            # Aplica ε-fecho
            atuais = self.epsilon_fecho(proximos)
            print(f"Após ler '{simbolo}' → possíveis estados: {atuais}")

        aceita = len(atuais & self.estados_aceitacao) > 0
        print("\nCadeia ACEITA!" if aceita else "\nCadeia REJEITADA!")
        return aceita

    def simular_cadeias(self):
        print("\n=== SIMULAÇÃO DE CADEIAS ===")
        while True:
            cadeia = input("Cadeia (ou 'sair'): ").strip()
            if cadeia.lower() == "sair":
                break
            self.processar_cadeia(cadeia)

    def mostrar_afn(self):
        print("\n=== AFN DEFINIDO ===")
        print(f"Estados: {self.estados}")
        print(f"Alfabeto: {self.alfabeto}")
        print(f"Estado inicial: {self.estado_inicial}")
        print(f"Estados de aceitação: {self.estados_aceitacao}")
        print("Transições:")
        for (estado, simbolo), destinos in self.transicoes.items():
            print(f"  δ({estado}, {simbolo}) → {destinos}")
    
    def desenhar_afn(self):
        if not self.estados:
            print("AFN não definido.")
            return

        print("\n=== DESENHO ASCII DO AFN ===\n")

        # Marca finais com '*'
        def marca_final(s):
            return s + "*" if s in self.estados_aceitacao else s

        # Ordena para ficar mais bonito
        estados_ordenados = sorted(list(self.estados))

        for estado in estados_ordenados:
            nome_estado = marca_final(estado)
            print(f"{nome_estado}")

            # Todas transições do estado
            trans = []
            for (orig, simb), destinos in self.transicoes.items():
                if orig == estado:
                    for d in destinos:
                        trans.append((simb, d))

            if not trans:
                print("   (sem transições)\n")
                continue

            # Primeira transição desenhada na horizontal
            simb0, dest0 = trans[0]
            simb0 = "ε" if simb0 == "ε" else simb0
            print(f"   --{simb0}--> {marca_final(dest0)}")

            # As demais viram ramificações com "\" no início
            for simb, dest in trans[1:]:
                simb = "ε" if simb == "ε" else simb
                print(f"   \\--{simb}--> {marca_final(dest)}")

            print()

        print("=================================\n")




def main():
    afn = AFN()
    
    while True:
        print("\n" + "="*50)
        print("          SIMULADOR DE AFN")
        print("="*50)
        print("1. Definir novo AFN")
        print("2. Mostrar AFN atual")
        print("3. Desenhar AFN (gerar imagem)")
        print("4. Simular cadeias")
        print("5. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            afn.ler_quintupla()
        elif opcao == "2":
            if afn.estados:
                afn.mostrar_afn()
            else:
                print("AFN não definido. Use a opção 1 primeiro.")
        elif opcao == "3":
            if afn.estados:
                afn.desenhar_afn()
            else:
                print("AFN não definido. Use a opção 1 primeiro.")
        elif opcao == "4":
            if afn.estados:
                afn.simular_cadeias()
            else:
                print("AFN não definido. Use a opção 1 primeiro.")
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()