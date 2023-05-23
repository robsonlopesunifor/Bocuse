from Bocuse.core.google_api import GoogleSheet


class FichaTecnica(GoogleSheet):
    def receita(self):
        return {
            "equipamentos": self.equipamentos(),
            "ingredientes": self.ingredientes(),
            "informacoes": self.informacoes(),
            "preparos": self.preparos(),
        }

    def ingredientes(self):
        data_frame = self.dataSheet("ingredientes")
        novas_chaves = data_frame.iloc[3:4, 0:].to_dict("records")
        novo_df = data_frame.iloc[4:, 0:].rename(columns=novas_chaves[0])
        ingredientes = novo_df.to_dict("records")
        grupos_ingredientes = []
        etapa = {}
        for index in range(len(ingredientes)):
            title_parte = ingredientes[index].pop("parte")
            if title_parte != "":
                etapa = {"etapa": title_parte, "ingredientes": [ingredientes[index].copy()]}
            else:
                etapa["ingredientes"].append(ingredientes[index].copy())
            if len(ingredientes) == (index + 1) or ingredientes[index + 1]["parte"] != "":
                grupos_ingredientes.append(etapa)
        return grupos_ingredientes

    def informacoes(self):
        data_frame = self.dataSheet("ingredientes")
        novas_chaves = data_frame.iloc[1:2, 0:].to_dict("records")
        novo_df = data_frame.iloc[2:3, 0:].rename(columns=novas_chaves[0])
        ingredientes = novo_df.to_dict("records")[0]
        return ingredientes

    def equipamentos(self):
        data_frame = self.dataSheet("equipamentos")
        equipamentos = dict(data_frame.iloc[1:, 0:].values)
        lista_equipamentos = []
        for key in equipamentos:
            equipamentos[key] = True if equipamentos[key] == "1" else False
            lista_equipamentos.append({"nome": key, "necessario": equipamentos[key]})
        return lista_equipamentos

    def preparos(self):
        data_frame = self.dataSheet("preparos")
        preparos = data_frame.to_dict("records")
        grupos_preparos = []
        parte = {}
        for index in range(len(preparos)):
            etapa = preparos[index][0]
            passo = preparos[index][1]
            if etapa == "etapa":
                parte = {"etapa": passo, "passos": []}
            else:
                parte["passos"].append({"descricao": passo, "tipo": etapa})
            if len(preparos) == (index + 1) or preparos[index + 1][0] == "etapa":
                grupos_preparos.append(parte)
        return grupos_preparos
