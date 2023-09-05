import { observer } from 'mobx-react-lite';
import { AuthPage, AuthPageS } from '/src/auth/components/AuthPage';
import { RequestMagicLinkCard } from '/src/auth/components/RequestMagicLinkCard';
import { SignInLogo } from '/src/frames/components/SignInLogo';
import { cn } from '/src/utils/classnames';

export const RequestMagicLinkPage = observer(() => {
  return (
    <AuthPage>
      <SignInLogo />
      <div className={cn(AuthPageS.Gap())} />
      <RequestMagicLinkCard />
    </AuthPage>
  );
});
