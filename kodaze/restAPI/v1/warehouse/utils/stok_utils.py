from rest_framework import status
from rest_framework.response import Response

def stok_update(self, request, *args, **kwargs):
    stok = self.get_object()
    serializer = self.get_serializer(stok, data=request.data, partial=True)
    say = int(request.data.get("say"))

    if serializer.is_valid():
        serializer.save(say=say)
        return Response({"detail" : "Məlumatlar yeniləndi"}, status=status.HTTP_200_OK)
    else:
        return Response({"detail" : "Xəta baş verdi!"}, status=status.HTTP_400_BAD_REQUEST)
    # try:
    #     # stok = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)

    #     stok.say = stok.say + say
    #     stok.save()
    #     # super(StokSerializer, self).update(request, *args, **kwargs)
    #     return Response({"detail" : "Məlumatlar yeniləndi"}, status=status.HTTP_200_OK)
    # except:
    #     return Response({"detail" : "Problem"}, status=status.HTTP_400_BAD_REQUEST)