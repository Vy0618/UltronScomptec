import { Link } from "react-router-dom";

export default function PasswordHelp() {
  return (
    <main className="flex min-h-svh items-center justify-center p-4">
      <section className="panel w-full max-w-md space-y-4 p-6">
        <h1 className="text-xl font-bold">Recuperar acesso</h1>
        <p className="text-sm leading-relaxed text-text-secondary">
          Solicite ao administrador da sua instalação a redefinição da senha.
          Informe o e-mail usado no cadastro para que ele identifique sua conta.
        </p>
        <p className="text-sm text-text-muted">
          A recuperação por e-mail ainda não está disponível nesta instalação.
        </p>
        <Link to="/login" className="btn-primary">
          Voltar para o login
        </Link>
      </section>
    </main>
  );
}
