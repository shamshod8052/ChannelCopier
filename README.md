**README.md**  

# **ChannelCopier**  

## **Loyiha haqida**  
ChannelCopier — bu Telegram kanallardan xabarlarni boshqa kanallarga real vaqt rejimida nusxalash uchun ishlab chiqilgan loyiha.  

---

## **Ishga tushirish**  

1. **`.env` faylini yaratish:**  
   `.env.example` → `.env`  
   - `INTERVAL_SECONDS` – Xabarlarni nusxalash oraliq vaqti (sekundlarda).  
   - `COPY_START_TIME` – Dastur ishga tushganda nusxalashni necha sekund oldingi xabardan boshlash kerakligi.  

2. **Ma’lumotlar bazasini yaratish**  

3. **Virtual muhitni ishga tushirish va kerakli kutubxonalarni o‘rnatish**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # (Windows uchun: venv\Scripts\activate)
   pip install -r requirements.txt
   ```

4. **Ma’lumotlar bazasini sozlash**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Superuser yaratish**  
   ```bash
   python manage.py createsuperuser
   ```

6. **Dastur serverini ishga tushirish**  
   ```bash
   python manage.py runserver
   ```

7. **Telegram client (user bot) ni ishga tushirish**  
   ```bash
   python run_user_bot.py
   ```

---

## **Admin panel tushuntirishlari**  

1. **Users** – Foydalanuvchilar jadvali  
   - `Process status` – `True` holatiga o‘tkazilsa, xabar nusxalash jarayoni boshlanadi.  

2. **Channels** – Barcha jarayonda qatnashadigan kanallarni qo‘shish.  

3. **Senders** – Xabar ko‘chiriladigan kanallarni belgilash.  

4. **Getters** – Xabar yuboriladigan kanallarni belgilash.  

5. **ExtraTexts** – Ko‘chirilgan xabarlardagi havolalarni o‘zgartirish uchun  
   - `status` – `True` bo‘lsa, matnni almashtirish mumkin.  

---

## **Xabarlarni tozalash (Message cleaner)**  

- **Telefon raqamlari (O‘zbekiston)**  
  ```python
  PHONE_PATTERN_UZ = r'\+?998([- .])?(90|91|93|94|95|98|99|33|97|71)([- .])?(\d{3})([- .])?(\d{2})([- .])?(\d{2})'
  ```
- **Telegram foydalanuvchi nomlari**  
  ```python
  USERNAME_PATTERN = r'@\w+'
  ```
- **URL manzillar**  
  ```python
  URL_PATTERN = r'(?:http[s]?://|www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(?:/[^\s]*)?'
  ```
