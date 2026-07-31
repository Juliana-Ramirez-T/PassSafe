from collections import defaultdict


class SecurityAuditService:
    @staticmethod
    def analyze(credentials):
        credentials = list(credentials)
        weak_list = [credential for credential in credentials
                     if len(credential.password) < 8
                     or credential.password.isalpha()
                     or credential.password.isdigit()]

        password_map = defaultdict(list)
        for credential in credentials:
            password_map[credential.password].append(credential)

        reused_list = []
        for group in password_map.values():
            if len(group) > 1:
                reused_list.extend(group)

        weak_count = len(weak_list)
        reused_count = len({credential.password for credential in reused_list})
        total = len(credentials)
        score = 100 if total == 0 else max(0, 100 - weak_count * 10 - reused_count * 5)

        recommendations = []
        if total == 0:
            recommendations.append('Agrega tus primeras credenciales para iniciar la auditoría.')
        else:
            if weak_count:
                recommendations.append('Actualiza las contraseñas débiles cuanto antes.')
            if reused_count:
                recommendations.append('No reutilices la misma contraseña en varios servicios.')
            if not weak_count and not reused_count:
                recommendations.append('Excelente trabajo. Mantén tus contraseñas seguras y únicas.')

        return {
            'credentials': credentials,
            'total': total,
            'weak_count': weak_count,
            'reused_count': reused_count,
            'score': score,
            'recommendations': recommendations,
            'weak_list': weak_list,
            'reused_list': reused_list,
        }
