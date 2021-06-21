import { normalize, schema } from 'normalizr';
import { ApiBase } from 'src/api/ApiBase';
import { ObjT } from 'src/utils/types';

const milestone = new schema.Entity('milestones');
const milestoneList = new schema.Array(milestone);
const project = new schema.Entity('projects', { milestones: milestoneList });

export class Api extends ApiBase {
  loadProjectBySlug(slug: string) {
    return this._doQuery(
      'loadProjectBySlug',
      `query loadProjectBySlug(
      $slug: String
    ) {
      project(
        slug: $slug
      ) {
        id
        name
        imageHash
        imageProps
        content
        milestones {
          id
          name
          content
          isCompleted
        }
      }
    }`,
      { slug },
      (response: ObjT) => normalize(response.project, project).entities,
      (error: ObjT) => error.response.errors[0].message
    );
  }
}
