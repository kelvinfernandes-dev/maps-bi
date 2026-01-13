# Salva com padrão brasileiro: separador de campo ; e decimal ,
df.to_csv("dados_geolocalizados.csv", index=False, sep=';', decimal=',')

# No final do seu script, tente salvar direto em Excel para manter a precisão:
df.to_excel("dados_geolocalizados_final.xlsx", index=False)
