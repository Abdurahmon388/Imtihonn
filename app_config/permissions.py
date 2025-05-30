from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminUser(permissions.BasePermission):
    """
    Faqat admin (superuser) bo'lgan foydalanuvchilarga ruxsat beradi.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class AdminOrOwner(BasePermission):
    """
    Foydalanuvchi admin bo‘lsa yoki o‘ziga tegishli ma'lumotga kirsa, ruxsat beriladi.
    """

    def has_object_permission(self, request, view, obj):
        # Faqat ko‘rish (GET, HEAD, OPTIONS) ruxsat beriladi
        if request.method in SAFE_METHODS:
            return True

        # Admin foydalanuvchilarga ruxsat beriladi
        if request.user.is_staff:
            return True

        # Foydalanuvchi o‘zining obyektini tahrirlashiga ruxsat
        return obj.owner == request.user

class IsAdminOrOwner(BasePermission):
    """
    Faqat admin yoki o‘ziga tegishli ob'ektga ruxsat berish.
    """
    def has_object_permission(self, request, view, obj):
        return bool(request.user and (request.user.is_staff or obj.owner == request.user))


class IsAdminUser(BasePermission):
    """
    Faqat admin foydalanuvchilarga ruxsat beradi.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class IsAuthenticated(BasePermission):
    """
    Faqat ro‘yxatdan o‘tgan foydalanuvchilarga ruxsat beradi.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsOwnerOrReadOnly(BasePermission):
    """
    Ob'ektning egasiga o‘zgartirish va o‘chirishga ruxsat beradi, 
    boshqalarga faqat o‘qish huquqini beradi.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsAdminOrReadOnly(BasePermission):
    """
    Agar foydalanuvchi admin bo‘lsa, barcha ruxsat beriladi.
    Oddiy foydalanuvchilar faqat GET (ko‘rish) imkoniyatiga ega.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True  # Hamma ko‘ra oladi
        return request.user and request.user.is_staff  

class IsAuthenticatedUser(permissions.BasePermission):
    """
    Faqat autentifikatsiya qilingan foydalanuvchilarga ruxsat beradi.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated




class AllowAny(permissions.BasePermission):
    """
    Har qanday foydalanuvchiga ruxsat beradi (autentifikatsiya shart emas).
    """
    def has_permission(self, request, view):
        return True
