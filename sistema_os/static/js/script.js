/**
 * Script de Gerenciamento do Cadastro de Clientes
 * Funções:
 * 1. Busca automática de CEP
 * 2. Validação de formulário
 * 3. Máscaras para campos
 */

document.addEventListener('DOMContentLoaded', function() {
    // Configura máscaras para os campos
    aplicarMascaras();
    
    // Busca CEP quando o campo perde o foco
    document.getElementById('cep').addEventListener('blur', buscarCEP);
    
    // Valida o formulário antes do envio
    document.querySelector('form').addEventListener('submit', validarFormulario);
});

// Aplica máscaras aos campos
function aplicarMascaras() {
    // Máscara para CPF/CNPJ
    $('#cnpj_cpf').inputmask({
        mask: ['999.999.999-99', '99.999.999/9999-99'],
        keepStatic: true
    });

    // Máscara para telefone
    $('#telefone').inputmask('(99) 99999-9999');

    // Máscara para CEP
    $('#cep').inputmask('99999-999');
}

// Busca dados do CEP
async function buscarCEP() {
    const cep = document.getElementById('cep').value.replace(/\D/g, '');
    const campos = {
        rua: document.getElementById('rua'),
        bairro: document.getElementById('bairro'),
        cidade: document.getElementById('cidade')
    };

    if (cep.length !== 8) {
        mostrarNotificacao('CEP inválido', 'error');
        return;
    }

    try {
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const data = await response.json();

        if (data.erro) {
            throw new Error('CEP não encontrado');
        }

        // Preenche os campos automaticamente
        campos.rua.value = data.logradouro || '';
        campos.bairro.value = data.bairro || '';
        campos.cidade.value = data.localidade || '';
        
        mostrarNotificacao('CEP encontrado!', 'success');
    } catch (error) {
        console.error('Erro na busca do CEP:', error);
        mostrarNotificacao(error.message, 'error');
    }
}

// Validação do formulário
function validarFormulario(event) {
    const form = event.target;
    let valido = true;

    // Valida CPF/CNPJ
    const cnpjCpf = document.getElementById('cnpj_cpf').value.replace(/\D/g, '');
    const tipoCliente = document.getElementById('tipoCliente').value;
    
    if (tipoCliente === 'PF' && cnpjCpf.length !== 11) {
        mostrarNotificacao('CPF inválido', 'error');
        valido = false;
    } else if (tipoCliente === 'PJ' && cnpjCpf.length !== 14) {
        mostrarNotificacao('CNPJ inválido', 'error');
        valido = false;
    }

    // Valida e-mail
    const email = document.getElementById('email').value;
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        mostrarNotificacao('E-mail inválido', 'error');
        valido = false;
    }

    if (!valido) {
        event.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Exibe notificações
function mostrarNotificacao(mensagem, tipo = 'info') {
    const cores = {
        success: '#2ecc71',
        error: '#e74c3c',
        info: '#3498db'
    };

    Toastify({
        text: mensagem,
        duration: 3000,
        close: true,
        gravity: "top",
        position: "right",
        backgroundColor: cores[tipo] || cores.info,
        stopOnFocus: true
    }).showToast();
}