from django.core.exceptions import ValidationError
from django.forms import ModelForm
from catalog.models import Product


class ProductForm(ModelForm):
    restricted_list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                       'радар']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите цену'
        })

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price',)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            for word in self.restricted_list:
                if word in name.lower():
                    raise ValidationError(f'Название продукта не может содержать слово "{word}"')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            for word in self.restricted_list:
                if word in description.lower():
                    raise ValidationError(f'Описание продукта не может содержать слово "{word}"')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price:
            if price < 0:
                raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        allowed_extensions_list = ['png', 'jpeg', 'jpg']
        extension_flag = False
        if image:
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError("Размер изображения не должен превышать 5 МБ.")

            for extension in allowed_extensions_list:
                if str(image).lower().endswith(extension):
                    extension_flag = True
            if not extension_flag:
                raise ValidationError('Файл может быть только с разрешением "png" или "jpg"')
        return image
