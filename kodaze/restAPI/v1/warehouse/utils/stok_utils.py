from rest_framework import status
from rest_framework.response import Response

def stok_update(self, request, *args, **kwargs):
    stok = self.get_object()
    serializer = self.get_serializer(stok, data=request.data, partial=True)
    mehsul_id = request.data.get("mehsul_id")
    say = int(request.data.get("say"))
    anbar_id = request.data.get("anbar_id")

    # mehsul = get_object_or_404(Mehsullar, pk=mehsul_id)
    # anbar = get_object_or_404(Anbar, pk=anbar_id)
    try:
        # stok = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)

        stok.say = stok.say + say
        stok.save()
        # super(StokSerializer, self).update(request, *args, **kwargs)
        return Response({"detail" : "Məlumatlar yeniləndi"}, status=status.HTTP_200_OK)
    except:
        return Response({"Problem"}, status=status.HTTP_404_NOT_FOUND)