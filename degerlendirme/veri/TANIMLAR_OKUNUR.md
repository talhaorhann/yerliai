# Gizli yapısal tanımlar (V-019, okuma için)

Asıl veri: `degerlendirme/veri/tanimlar_v1.json`. Bu dosya `degerlendirme.dunya.okunur_tanimlar` çıktısıdır.
GİZLİ KURALLAR (kâhin). Yalnız degerlendirme/ okur. Adım: yon U=ebeveyne, D=çocuğa, E=eşe; tip ulaşılan kişinin tipi (null=fark etmez). Bir ilişki, A'dan B'ye kişi tekrarlamayan bir yürüyüş adımlara uyuyorsa vardır. Tip 1 = erkek, tip 0 = kadın.

Okuma: "A'nın ebeveyni (tip 1) → onun ebeveyni" = A'nın babasının bir ebeveyni.
Doğrudan olgu olarak verilen ilişkiler: anne, baba, oğul, kız, eş, erkek_kardeş, kız_kardeş

| İlişki | B, A'nın ... (adım adım) |
|---|---|
| anne | ebeveyni (tip 0) |
| baba | ebeveyni (tip 1) |
| oğul | çocuğu (tip 1) |
| kız | çocuğu (tip 0) |
| eş | evlendiği kişi |
| erkek_kardeş | ebeveyni → çocuğu (tip 1) |
| kız_kardeş | ebeveyni → çocuğu (tip 0) |
| dede | ebeveyni → ebeveyni (tip 1) |
| babaanne | ebeveyni (tip 1) → ebeveyni (tip 0) |
| anneanne | ebeveyni (tip 0) → ebeveyni (tip 0) |
| torun | çocuğu → çocuğu |
| amca | ebeveyni (tip 1) → ebeveyni → çocuğu (tip 1) |
| dayı | ebeveyni (tip 0) → ebeveyni → çocuğu (tip 1) |
| hala | ebeveyni (tip 1) → ebeveyni → çocuğu (tip 0) |
| teyze | ebeveyni (tip 0) → ebeveyni → çocuğu (tip 0) |
| yeğen | ebeveyni → çocuğu → çocuğu |
| kuzen | ebeveyni → ebeveyni → çocuğu → çocuğu |
| kayınpeder | evlendiği kişi → ebeveyni (tip 1) |
| kayınvalide | evlendiği kişi → ebeveyni (tip 0) |
| gelin | çocuğu (tip 1) → evlendiği kişi |
| damat | çocuğu (tip 0) → evlendiği kişi |
