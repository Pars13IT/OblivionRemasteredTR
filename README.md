# Oblivion Remastered Türkçe Yama

Bu proje [MagicLoader 2](https://www.nexusmods.com/oblivionremastered/mods/1966) yardımı ile Oblivion Remastered oyununu Türkçe'ye çevirmeyi amaçlamaktadır. Game.locres dosyası [Important On Top](https://www.nexusmods.com/oblivionremastered/mods/2160) modu ile gelen pak dosyasından ayıklanmıştır.

Proje sonlandığında bu dosya, klavuz olarak değiştirilip yerine sadece projeyi anlatan bir readme hazırlanacaktır.

Kendiniz deneyimlemek isterseniz aşağıdaki kodu kullanabilirsiniz.

```cmd
UnrealPak.exe "<KaynakKlasör>\z_Important_On_Top_P.pak" -Extract <HedefKlasör>
```

UnrealPak.exe UnrealEngine ile gelmektedir. UE kurulumunu yaptıktan sonra PATH ortam değişkenine `<KurulumKlasörü>\UE_5.5\Engine\Binaries\Win64` yolunu eklemelisiniz.

Locres'i [UnrealLocres](https://github.com/akintos/UnrealLocres/releases) ile csv ya da pot dosyasına dönüştürebiliyoruz. Metinlerde virgül kullanıldığı için, virgül ile ayrılmış csv dosyasını işlemek yerine pot dosyasına çevirmeye karar verdim.

```cmd
UnrealLocres.exe export <KaynakKlasör>\Game.locres -f pot -o <HedefKlasör>\Game.pot
```

Test ettiğimde aşağıdaki json dosyasının, "...Oblivion Remastered\OblivionRemastered\Content\Dev\ObvData\Data\MagicLoader" klasörüne konduğunda işe yaradığını gördüm. Steam versiyonunda test ettim ama muhtemelen GamePass ile de çalışacaktır.

```json
{
    "AltarDynamicTexts":{
        "LOC_AD_Persuasion_Notification_BribeValueCost": " <img id=\"Disposition\"/>  +{Disposition} eğilim\n <img id=\"ArrowRight\"/> {Cost}"
    }
}
```
Aşağıdaki veriyi yukarıdaki json standardına çevirmek vim macrolar ile pek de zor olmayacaktır.

```pot
msgctxt "ST_AltarDynamicTexts/LOC_AD_Persuasion_Notification_BribeValueCost"
msgid ""
" <img id=\"Disposition\"/>  +{Disposition} disposition\n"
" <img id=\"ArrowRight\"/> {Cost}"
msgstr ""
```


