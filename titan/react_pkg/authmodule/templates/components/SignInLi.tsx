import { RouterLink } from '/src/routes/components';
import { useRoutes } from '/src/routes/hooks/useRoutes';

type PropsT = {
  menuHandler: any;
};

export const SignInLi = (props: PropsT) => {
  const routes = useRoutes();

  return (
    <li className="uk-active">
      <RouterLink
        to={routes.signIn()}
        onClick={props.menuHandler.closeDropDown}
      >
        Sign in
      </RouterLink>
    </li>
  );
};
