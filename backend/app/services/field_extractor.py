import re
from typing import List, Dict, Any, Tuple


class FieldExtractor:
    """Extrai campos {campo_nome} do conteúdo do template"""

    FIELD_PATTERN = r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}'

    @staticmethod
    def extract_fields(content: str) -> List[Dict[str, Any]]:
        """
        Extrai todos os campos únicos do conteúdo
        Exemplo: "Olá {nome}, data: {data}" retorna [{"name": "nome"}, {"name": "data"}]
        """
        matches = re.findall(FieldExtractor.FIELD_PATTERN, content)
        unique_fields = list(dict.fromkeys(matches))  # Remove duplicatas mantendo ordem

        fields = []
        for field_name in unique_fields:
            fields.append({
                "name": field_name,
                "field_type": FieldExtractor._infer_type(field_name),
                "required": True
            })

        return fields

    @staticmethod
    def _infer_type(field_name: str) -> str:
        """Infere tipo de campo baseado no nome"""
        field_lower = field_name.lower()

        if "data" in field_lower or "date" in field_lower:
            return "date"
        elif "email" in field_lower:
            return "email"
        elif "telefone" in field_lower or "phone" in field_lower:
            return "text"
        elif "numero" in field_lower or "number" in field_lower:
            return "number"
        elif "valor" in field_lower or "price" in field_lower:
            return "number"

        return "text"

    @staticmethod
    def validate_fields(content: str, data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Valida se todos os campos necessários foram preenchidos
        Retorna (válido, mensagem_erro)
        """
        fields = FieldExtractor.extract_fields(content)

        for field in fields:
            field_name = field["name"]
            if field_name not in data or data[field_name] is None:
                return False, f"Campo '{field_name}' é obrigatório"

        return True, ""

    @staticmethod
    def replace_fields(content: str, data: Dict[str, Any]) -> str:
        """
        Substitui todos os campos {campo} pelos valores fornecidos
        """
        result = content

        for field_name, value in data.items():
            placeholder = "{" + field_name + "}"
            result = result.replace(placeholder, str(value))

        return result

    @staticmethod
    def has_unreplaced_fields(content: str) -> bool:
        """Verifica se ainda há campos não substituídos"""
        return bool(re.search(FieldExtractor.FIELD_PATTERN, content))

    @staticmethod
    def get_unreplaced_field_names(content: str) -> List[str]:
        """Retorna lista de campos ainda não substituídos"""
        return re.findall(FieldExtractor.FIELD_PATTERN, content)
