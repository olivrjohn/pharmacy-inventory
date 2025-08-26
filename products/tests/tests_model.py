from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import ProductCategory, MedicineType, Product


# NOTE! create test for string representation, using symbols, etc.

# Create your tests here.
class ProductCategoryTestCase(TestCase):
    """Test cases for Product Category text choices"""
    def test_product_category_correct_values(self):
        self.assertEqual(ProductCategory.GENERAL_GOODS, "GG")
        self.assertEqual(ProductCategory.MEDICINE, "MEDICINE")

    def test_product_category_correct_labels(self):
        self.assertEqual(ProductCategory.GENERAL_GOODS.label, "General Goods")
        self.assertEqual(ProductCategory.MEDICINE.label, "Medicine")

    def test_product_category_expected_choices(self):
        expected_values = ["GG", "MEDICINE"]
        self.assertCountEqual(ProductCategory.values, expected_values)
        
    def test_product_category_no_duplicate_values(self):
        self.assertEqual(len(ProductCategory.values), len(set(ProductCategory.values)))

    def test_product_category_no_duplicate_labels(self):
        self.assertEqual(len(ProductCategory.labels), len(set(ProductCategory.labels)))

class MedicineTypeTestCase(TestCase):
    """Test cases for Medicine Type text choices"""
    def test_medicine_type_correct_values(self):
        self.assertEqual(MedicineType.OTC, "OTC")
        self.assertEqual(MedicineType.PRESCRIPTION, "PRESCRIPTION")

    def test_medicine_type_correct_labels(self):
        self.assertEqual(MedicineType.OTC.label, "Over-the-counter")
        self.assertEqual(MedicineType.PRESCRIPTION.label, "Prescription Drugs")

    def test_medicine_type_expected_choices(self):
        expected_values = ["OTC", "PRESCRIPTION"]
        self.assertCountEqual(MedicineType.values, expected_values)

    def test_medicine_type_no_duplicate_values(self):
        self.assertEqual(len(MedicineType.values), len(set(MedicineType.values)))

    def test_medicine_type_no_duplicate_labels(self):
        self.assertEqual(len(MedicineType.labels), len(set(MedicineType.labels)))

class ProductFieldTestCase(TestCase):
    """These tests for fields inside the Product Model to verify the constraints, integrity, and correctness of data"""
    # Boilerplate; helper method that helps not to repeat the instances of Product values
    def create_product(self, **kwargs):
        defaults = {"brand": "Nike", "name": "test"}
        defaults.update(kwargs)

         # I need to use Product() to instantiate the model without saving it in the database so it won't avoid model-level validation of full_clean()
        return Product(**defaults)
    
    # Valid 'brand' field tests
    def test_brand_valid_within_max_length(self):
        """Test if the brand with characters within the max length limit is valid."""
        brand = "a" * 150
        instance = self.create_product(brand=brand)

        try:
            instance.full_clean()
        except ValidationError:
            self.fail("Brand that is within max length should be valid.")
   
    # Invalid 'brand' field tests
    def test_brand_invalid_over_max_length(self):
        """Test if the brand with characaters over the max length will raise an exception and will not be valid."""
        brand = "a" * 151
        instance = self.create_product(brand=brand)

        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()

        self.assertIn("brand", cm.exception.error_dict)

    def test_brand_invalid_empty(self):
        """Test if the brand that is empty is not valid."""
        instance = self.create_product(brand="")
        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()
    
        self.assertIn("brand", cm.exception.error_dict)

    def test_brand_invalid_none(self):
        """Test if the brand that has a value of None is not valid."""
        instance = self.create_product(brand=None)
        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()

        # Note to self. I still don't quite understand how this works but I know that it checks if in the context of the Validation Error raised during the full_clean() the right field, in this case "brand", is the one making that validation error
        self.assertIn("brand", cm.exception.error_dict)

    # Valid 'name' field tests
    def test_name_valid_within_max_length(self):
        """Test the 'name' field of the product model that have characters within max length."""

        name = "a" * 150
        instance = self.create_product(name=name)

        try:
            instance.full_clean()
        except ValidationError:
            self.fail("Name that is within max length should be valid.")

    # Invalid 'name' field tests
    def test_name_invalid_over_max_length(self):
        """Test the 'name' field of the product model that have characters over the max length."""

        name = "a" * 151
        instance = self.create_product(name=name)

        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()

        self.assertIn("name", cm.exception.error_dict)

    def test_name_invalid_empty(self):
        """Test the 'name' field of the product model that passes an emptly value."""

        instance = self.create_product(name="")

        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()

        self.assertIn("name", cm.exception.error_dict)
        
    def test_name_invalid_none(self):
        """Test the 'name' field of the product model that passes a value of 'None'."""

        instance = self.create_product(name=None)

        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()

        self.assertIn("name", cm.exception.error_dict)

    # Valid 'category' field tests
    def test_category_valid_within_max_length(self):
        """Test 'category' field of the product model that have characters within max length."""

        instance = self.create_product(category="MEDICINE")

        try:
            instance.full_clean()
        except ValidationError:
            self.fail("Category that is whithin max length should be valid.")

    def test_category_valid_default_value(self):
        """Test 'category' field of the product model to insert default value when no value is passed on the field."""

        instance = self.create_product()

        self.assertEqual(instance.category, "MEDICINE")

    # Invalid 'category' field tests
    def test_category_invalid_over_max_length(self):
        """Test 'category' field of the product model with characters over max length."""

        instance = self.create_product(category="MEDICINESSSS")

        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()
        
        self.assertIn("category", cm.exception.error_dict)

    def test_category_invalid_not_in_choices(self):
        """Test 'category' field of the product model with passed value not in expected choices."""

        instance = self.create_product(category="CLOTHING")

        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()

        self.assertIn("category", cm.exception.error_dict)

    def test_category_display_label(self):
        """Test 'category' frield of the product model to verify it shows the correct label of the text choice."""

        instance = self.create_product()

        # get_category_display() / get_foo_display() : for every field that has choices set, the object will get this method which returns the human-readable value of the field
        self.assertEqual(instance.get_category_display(), "Medicine")

    # Valid 'status' field tests
    def test_status_within_max_length(self):
        """Test 'status' field of product model that have characters within the max length."""

        status = "a" * 15
        instance = self.create_product(status=status)

        try:
            instance.full_clean()
        except ValidationError:
            self.fail("Status that is within max length should be valid.")

    def test_status_default_value(self):
        """Test 'status' field of product model if it sets the value to 'DRAFT' when no value is passed."""

        instance = self.create_product()
        self.assertEqual(instance.status, "DRAFT")

    # Invalid 'status' field tests
    def test_status_invalid_over_max_length(self):
        """Test 'status' field of the product model if the character limit have been exceeded."""

        status = "a" * 16
        instance = self.create_product(status=status)

        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()

        self.assertIn("status", cm.exception.error_dict)

    def test_status_invalid_empty(self):
        """Test 'status' field of the product model if empty value is passed."""

        instance = self.create_product(status="")

        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()

        self.assertIn("status", cm.exception.error_dict)

    def test_status_invalid_none(self):
        """Test 'status' field of the product model if 'None' is passed."""

        instance = self.create_product(status=None)

        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()

        self.assertIn("status", cm.exception.error_dict)