import { SignupForm } from "@/components/signup-form";

export default function SignupPage() {
    return (
        <div className="flex min-h-svh flex-col items-center justify-center gap-6 bg-muted w-full">
            <div className="flex w-full max-w-sm flex-col gap-6">
                <SignupForm />
            </div>
        </div>
    );
}
