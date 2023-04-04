from Menu.core.google_api import GoogleSheet


class FichaTecnica(GoogleSheet):
    def fichaTecnica(self):
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
        for key in equipamentos:
            equipamentos[key] = True if equipamentos[key] == "1" else False
        return equipamentos

    def preparos(self):
        etapa = []
        preparos = []
        data_frame = self.dataSheet("preparos")
        for _, row in data_frame.iterrows():
            if row[0] == "etapa" and etapa:
                preparos.append(etapa.copy())
                etapa = []
            if row[1]:
                etapa.append((row[0], row[1]))
        preparos.append(etapa.copy())
        return preparos
