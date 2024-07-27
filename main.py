import os

import click
from ghapi.all import GhApi
from ghapi.page import paged


@click.command()
@click.option('--dry/--no-dry', default=False, help="Don't do any deletions (dry run).")
@click.option('--token',
              default=lambda: os.environ.get('GITHUB_TOKEN'),
              type=str,
              help="GitHub Personal Access Token to use. Can also be set via the GITHUB_TOKEN environment variable.",
              required=True)
def main(dry, token):
    api = GhApi(authenticate=True, token=token)

    results = paged(api.codespaces.list_for_authenticated_user)
    organization_to_spaces = {}
    for page in results:
        for codespace in page['codespaces']:
            billable_owner = codespace['billable_owner']
            billable_owner_type = billable_owner['type']
            if billable_owner_type == 'Organization':
                billable_owner_name = billable_owner['login']
                if billable_owner_name not in organization_to_spaces:
                    click.echo(f'Discovered new organization: {billable_owner_name}...')
                    organization_to_spaces[billable_owner_name] = set()

                organization_to_spaces[billable_owner_name].add(codespace['name'])
        else:
            break

    click.echo()

    org_list = sorted(organization_to_spaces.keys())
    max_num = len(org_list)
    max_num_w = str(max_num)
    for idx, org in enumerate(org_list):
        click.echo(f'{1 + idx: >{max_num_w}}) {org}')

    org_ind = click.prompt("Choose an organization [0 to cancel]", type=click.IntRange(0, max_num)) - 1

    if org_ind < 0:
        return

    org = org_list[org_ind]

    for codespace in organization_to_spaces[org]:
        click.echo(f'Deleting {codespace}...')
        if not dry:
            api.codespaces.delete(codespace)

    click.echo('Done!')


if __name__ == '__main__':
    main()
